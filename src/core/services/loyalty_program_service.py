# pylint: disable=import-outside-toplevel

from decimal import Decimal
from random import randint
from typing import Optional

from django.db.models import Q, Sum

from core.models import (
    LoyaltyProgram,
    LoyaltyProgramIncome,
    LoyaltyProgramPayout,
    User,
    WebinarApplication,
)
from core.models.enums import (
    ApplicationStatus,
    LoyaltyProgramIncomeStatus,
    LoyaltyProgramPayoutStatus,
)


class LoyaltyProgramService:
    """Loyality program service"""

    MIN_PAYOUT_VALUE = 150

    def __init__(self, user: User) -> None:
        self.user = user

    @staticmethod
    def generate_unused_ref_number() -> str:
        """Get unused ref number"""
        for _ in range(1_000):
            candidate = str(randint(10_000, 99_999))
            exists = LoyaltyProgram.manager.filter(
                ref_number=candidate
            ).exists()
            if not exists:
                return candidate
        return "1234567"  # low probability case

    @staticmethod
    def get_user_by_refcode(refcode: str) -> Optional[User]:
        """Get user by refocode

        Returns `None` if there is no user for given refcode
        """
        try:
            loyalty_program = LoyaltyProgram.manager.get(ref_number=refcode)
        except LoyaltyProgram.DoesNotExist:
            return None
        else:
            user: User = loyalty_program.user
            return user

    def loyalty_program_exists_for_user(self) -> bool:
        """Check if loyalty program exists for given user"""
        return LoyaltyProgram.manager.filter(user=self.user).exists()

    def get_or_create_loyalty_program(self):
        """Get or create loyality program for given user"""
        program_exists = self.loyalty_program_exists_for_user()

        if program_exists:
            loyalty_program = LoyaltyProgram.manager.get(user=self.user)
        else:
            loyalty_program = LoyaltyProgram(
                ref_number=self.generate_unused_ref_number(),
                user=self.user,
            )
            loyalty_program.save()

        return loyalty_program

    def get_all_user_incomes(self):
        """Get all user loyalty program incomes (all statuses)"""
        return LoyaltyProgramIncome.manager.filter(
            loyalty_program__user=self.user
        ).order_by("-created_at")

    def get_all_user_payouts(self):
        """Get all user payouts (all statuses)"""
        return LoyaltyProgramPayout.manager.filter(
            loyalty_program__user=self.user
        ).order_by("-created_at")

    def create_income_for_application(self, application: WebinarApplication):
        """Create income for given application"""
        loyalty_program = self.get_or_create_loyalty_program()

        from core.services import ApplicationService

        application_service = ApplicationService(application)

        provision_multiplier = round(loyalty_program.provision_percent / 100, 2)
        loyalty_program_income = LoyaltyProgramIncome(
            loyalty_program=loyalty_program,
            application=application,
            amount_brutto=round(
                application_service.get_total_price_netto()
                * provision_multiplier,
                2,
            ),
        )
        loyalty_program_income.save()

    def get_total_pending_income(self):
        """Get total pending income value for user"""
        ret: Decimal = (
            LoyaltyProgramIncome.manager.for_user(self.user)
            .filter(status=LoyaltyProgramIncomeStatus.PROCESSING)
            .aggregate(Sum("amount_brutto"))["amount_brutto__sum"]
        )

        return (ret or Decimal(0)).quantize(Decimal("1.00"))

    def get_total_payable_income(self):
        """Get total payable income value for user"""
        ret: Decimal = (
            LoyaltyProgramIncome.manager.for_user(self.user)
            .filter(status=LoyaltyProgramIncomeStatus.PAYABLE)
            .aggregate(Sum("amount_brutto"))["amount_brutto__sum"]
        )
        return (ret or Decimal(0)).quantize(Decimal("1.00"))

    def get_total_paid_payout(self):
        """Get total (paid) payout value for user"""
        ret: Decimal = (
            LoyaltyProgramPayout.manager.for_user(self.user)
            .filter(status=LoyaltyProgramPayoutStatus.PAYED)
            .aggregate(Sum("payout_brutto"))["payout_brutto__sum"]
        )
        return (ret or Decimal(0)).quantize(Decimal("1.00"))

    def get_total_pending_payout(self):
        """Get total (pending) payout value for user"""
        ret: Decimal = (
            LoyaltyProgramPayout.manager.for_user(self.user)
            .filter(status=LoyaltyProgramPayoutStatus.WAITING_FOR_CONFIRMATION)
            .aggregate(Sum("payout_brutto"))["payout_brutto__sum"]
        )
        return (ret or Decimal(0)).quantize(Decimal("1.00"))

    def get_available_payout_value(self) -> Decimal:
        """Get available payout value that will display next to payout form"""
        payable_income = self.get_total_payable_income()
        paid_payout = self.get_total_paid_payout()
        pending_payout = self.get_total_pending_payout()
        return payable_income - (paid_payout + pending_payout)

    def is_minimal_payout_value_reached(self) -> bool:
        """Checks if minimal payout value is reached"""
        return self.get_available_payout_value() >= self.MIN_PAYOUT_VALUE

    def can_create_payout_value(self, request_value: Decimal):
        """Check if payout value provided by user is valid"""

        if request_value > self.get_available_payout_value():
            msg = "Nie masz wystarczająco środków, aby wypłacić"
            return False, f"{msg} {request_value} zł"

        return True, "OK"

    def mark_payed_as_payable(self) -> None:
        """Mark incomes with payed application as payable"""
        LoyaltyProgramIncome.manager.for_user(self.user).filter(
            Q(application__status=ApplicationStatus.PAYED)
            & Q(status=LoyaltyProgramIncomeStatus.PROCESSING)
        ).update(status=LoyaltyProgramIncomeStatus.PAYABLE)

    def get_context(self):
        """Get context for loyalty program page dashboard"""
        loyalty_program = self.get_or_create_loyalty_program()
        total_pending_income = self.get_total_pending_income()
        total_payable_income = self.get_total_payable_income()
        total_paid_payout = self.get_total_paid_payout()
        total_pending_payout = self.get_total_pending_payout()
        available_payout_value = self.get_available_payout_value()
        return {
            "MIN_PAYOUT_VALUE": self.MIN_PAYOUT_VALUE,
            "loyalty_program": loyalty_program,
            "ref_code": loyalty_program.ref_number,
            "all_incomes": self.get_all_user_incomes(),
            "all_payouts": self.get_all_user_payouts(),
            "total_pending_income": total_pending_income,
            "total_payable_income": total_payable_income,
            "total_paid_payout": total_paid_payout,
            "total_pending_payout": total_pending_payout,
            "available_payout_value": available_payout_value,
            "reached_minium_payout": self.is_minimal_payout_value_reached(),
        }
