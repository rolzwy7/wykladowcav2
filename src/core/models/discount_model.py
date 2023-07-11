import uuid

from django.conf import settings
from django.db.models import (
    RESTRICT,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    OneToOneField,
    Q,
    QuerySet,
    TextField,
    UUIDField,
)
from django.utils.timezone import now

from .enums import DiscountCodeType, DiscountCodeUseType


class DiscountCodeManager(Manager):
    """Eventlog query Manager"""

    ...


class DiscountCode(Model):
    """Represents discount code"""

    manager = DiscountCodeManager()

    uuid = UUIDField(
        "Identyfikator kodu promocyjnego", default=uuid.uuid4, unique=True
    )

    discount_code = ...

    expired = BooleanField(
        "Zużyty", default=False, help_text="Kod został zużyty."
    )

    USE_TYPE = [
        (DiscountCodeUseType.ONE_TIME, "Jednorazowy"),
        (DiscountCodeUseType.MANY_TIMES, "Wielorazowy"),
    ]
    use_type = CharField("Typ użycia", choices=USE_TYPE)

    DISCOUNT_TYPE = [
        (DiscountCodeType.PERCENT, "( % ) Procentowa"),
        (DiscountCodeType.VALUE, "( zł ) Złotówkowa"),
    ]
    discount_type = CharField("Typ zniżki", choices=DISCOUNT_TYPE)

    expires = DateTimeField(
        "Zniżka wygasa",
        null=True,
        blank=True,
        help_text="Jeżeli nie ustawiono znaczy, że nie wygasa.",
    )

    class Meta:
        verbose_name = "Kod promocyjny"
        verbose_name_plural = "Kody promocyjne"


class DiscountApplicationApplied(Model):
    """Represents discounts applied to applications"""

    application = ForeignKey(
        "WebinarApplication", verbose_name="Zgłoszenie", on_delete=RESTRICT
    )

    discount_code = ForeignKey(
        "DiscountCode",
        verbose_name="Kod promocyjny",
        on_delete=RESTRICT,
        null=True,
        blank=True,
    )

    # code (optional)

    # - amount

    # desc

    class Meta:
        verbose_name = "Zniżka (zgłoszenie)"
        verbose_name_plural = "Zniżka (zgłoszenia)"


# class LoyaltyProgramIncome(Model):
#     """Represents loyality program income"""

#     created_at = DateTimeField(auto_now_add=True)

#     fk: LoyaltyProgram

#     fk: Application

#     status = ...  # realizacja, odmowiono, zrealizowano

#     amount = ...  # integer, brutto, netto ???

#     class Meta:
#         verbose_name = "Program partnerski (Należność)"
#         verbose_name_plural = "Program partnerski (Należności)"


# class LoyaltyProgramPayout(Model):
#     """Represents loyality program payout"""

#     created_at = DateTimeField(auto_now_add=True)

#     fk: LoyaltyProgram

#     status = ...  # realizacja, odmowiono, zrealizowano

#     amount = ...  # integer, brutto, netto ???

#     invoice_attachment = ...  # file

#     class Meta:
#         verbose_name = "Program partnerski (Wypłata)"
#         verbose_name_plural = "Program partnerski (Wypłaty)"
