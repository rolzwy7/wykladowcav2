from random import randint
from typing import Optional

from core.models import (
    LoyaltyProgram,
    LoyaltyProgramIncome,
    User,
    WebinarApplication,
)


class LoyaltyProgramService:
    """Loyality program service"""

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

    def get_user_incomes(self):
        """Get user loyalty program incomes"""
        return LoyaltyProgramIncome.objects.filter(
            loyalty_program__user=self.user
        )

    def create_income_for_application(self, application: WebinarApplication):
        """Create income for given application"""
        loyalty_program = self.get_or_create_loyalty_program()
        loyalty_program_income = LoyaltyProgramIncome(
            loyalty_program=loyalty_program,
            application=application,
            amount_brutto=round(
                application.total_price_netto
                * round(loyalty_program.provision_percent / 100, 2),
                2,
            ),
        )
        loyalty_program_income.save()
