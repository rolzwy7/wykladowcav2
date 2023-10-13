# flake8: noqa:E501
# pylint: disable=line-too-long
from random import choice, shuffle
from string import ascii_uppercase, digits

from django.db import transaction

from core.models import (
    DiscountApplicationApplied,
    DiscountCode,
    LoyaltyProgram,
    Webinar,
    WebinarApplication,
)
from core.models.enums import DiscountCodeType, DiscountCodeUseType


class DiscountService:
    """Discount service"""

    def __init__(self, application: WebinarApplication) -> None:
        self.application = application

    @staticmethod
    def generate_unused_discount_code(length: int = 8) -> str:
        """Generate unused discount code without saving it"""
        local_digits = digits
        local_digits = local_digits.replace("0", "")
        local_ascii_uppercase = ascii_uppercase
        local_ascii_uppercase = local_ascii_uppercase.replace("O", "")
        random_base = list(f"{local_ascii_uppercase}{local_digits}")
        shuffle(random_base)

        for _ in range(1_000):
            code_candid = "".join([choice(random_base) for _ in range(length)])
            code_already_exists = DiscountCode.manager.filter(
                discount_code=code_candid
            ).exists()
            if not code_already_exists:
                return code_candid
        return ""

    def get_application_discounts(self):
        """Get discounts for application"""
        return DiscountApplicationApplied.objects.filter(
            application=self.application
        )

    def get_application_discounts_total_weight(self):
        """Get total wieght of application discounts"""
        return sum(
            [
                application_discount.discount_weight
                for application_discount in self.get_application_discounts()
            ]
        )

    def are_further_discounts_allowed(self):
        """Are further discounts allowed to be applied"""
        return self.get_application_discounts_total_weight() < 1

    def is_refcode(self, code: str):
        """Check if provided code is a valid refcode of a user"""
        return LoyaltyProgram.manager.filter(ref_number=code).exists()

    def apply_refcode(self, refcode: str):
        """Apply refcode for this application"""

        # Save old netto price
        old_netto_price = self.application.price_netto

        # Apply loyalty program discount (5%)
        multiplier = (100 - 5) / 100
        new_price = int(multiplier * self.application.price_netto)
        self.application.price_netto = new_price

        # Set refcode in application
        self.application.refcode = refcode

        # Save application
        self.application.save()

        # Remember applied discount
        applied_discount = DiscountApplicationApplied(
            application=self.application,
            name="Kod referencyjny",
            description="Program lojalnościowy",
            amount=old_netto_price - self.application.price_netto,
        )
        applied_discount.save()

    def is_discount_code_valid(self, discount_code: str) -> bool:
        """Check if discount code is valid

        For discount code to be considered valid it must be present
        in database, not expired, not used if single use

        """
        return (
            DiscountCode.manager.valid_discount_codes()
            .filter(discount_code=discount_code)
            .exists()
        )

    def maybe_apply_initial_application_discount(self):
        """Apply initial discount to application if webinar is discounted"""

        webinar: Webinar = self.application.webinar
        if not webinar.is_discounted:
            return

        description = f"Promocja czasowa: {webinar.discount_netto}zł"
        description += f" zamiast {webinar.price_netto}zł"

        # Create application discount
        applied_application = DiscountApplicationApplied(
            application=self.application,
            discount_code=None,
            name="Promocja czasowa",
            description=description,
            discount_weight=0,
            amount=webinar.price_netto - webinar.discount_netto,
        )
        applied_application.save()

    def create_application_discount_from_code(self, discount_code: str):
        """Create discount for application

        Doesn't validate `discount_code`

        Args:
            discount_code (str): discount code
        """

        with transaction.atomic():
            # Get discount code from database
            discount_obj: DiscountCode = DiscountCode.manager.get(
                discount_code=discount_code
            )

            # Make description
            use_type_display = discount_obj.get_use_type_display()  # type: ignore
            discount_type_display = discount_obj.get_discount_type_display()  # type: ignore
            description = f"Kod promocyjny {use_type_display}"
            description += f", zniżka {discount_type_display}: {discount_obj.discount_value}"

            # Calculate discount
            old_netto_price = self.application.price_netto
            if discount_obj.discount_type == DiscountCodeType.VALUE:
                new_price = (
                    self.application.price_netto - discount_obj.discount_value
                )
                self.application.price_netto = new_price
            if discount_obj.discount_type == DiscountCodeType.PERCENT:
                multiplier = (100 - discount_obj.discount_value) / 100
                new_price = int(multiplier * self.application.price_netto)
                self.application.price_netto = new_price

            self.application.save()

            # Create application discount
            applied_discount = DiscountApplicationApplied(
                application=self.application,
                discount_code=discount_obj,
                name="Kod promocyjny",
                description=description,
                amount=old_netto_price - self.application.price_netto,
            )
            applied_discount.save()

            # If code is one time code then expired it
            if discount_obj.use_type == DiscountCodeUseType.ONE_TIME:
                discount_obj.expired = True
                discount_obj.save()

    def get_context(self):
        """Get context"""
        application_discounts = self.get_application_discounts()
        return {
            "application_discounts": application_discounts,
            "application_discounts_exists": application_discounts.exists(),
        }
