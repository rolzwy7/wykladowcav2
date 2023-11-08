import uuid

from django.db.models import (
    CASCADE,
    RESTRICT,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    PositiveSmallIntegerField,
    Q,
    QuerySet,
    SmallIntegerField,
    UUIDField,
)
from django.utils.timezone import now

from .enums import DiscountCodeType, DiscountCodeUseType


class DiscountCodeManager(Manager):
    """DiscountCode query Manager"""

    def valid_discount_codes(self) -> QuerySet["DiscountCode"]:
        """Get valid discount codes

        Returns:
            QuerySet["DiscountCode"]: valid discount codes
        """
        return self.get_queryset().filter(
            Q(expired=False) & (Q(expires__gte=now()) | Q(expires=None))
        )


class DiscountCode(Model):
    """Represents discount code"""

    manager = DiscountCodeManager()

    uuid = UUIDField("Identyfikator kodu promocyjnego", default=uuid.uuid4, unique=True)

    discount_code = CharField("Kod promocyjny", max_length=32, unique=True)

    discount_value = SmallIntegerField(
        "Wartość promocji",
        default=5,
        help_text="W zależności od typu. Albo `zł` albo `%`",
    )

    expired = BooleanField("Zużyty", default=False, help_text="Kod został zużyty.")

    USE_TYPE = [
        (DiscountCodeUseType.ONE_TIME, "Jednorazowy"),
        (DiscountCodeUseType.MANY_TIMES, "Wielorazowy"),
    ]
    use_type = CharField("Typ użycia", max_length=32, choices=USE_TYPE)

    DISCOUNT_TYPE = [
        (DiscountCodeType.PERCENT, "( % ) Procentowa"),
        (DiscountCodeType.VALUE, "( zł ) Złotówkowa"),
    ]
    discount_type = CharField("Typ zniżki", max_length=32, choices=DISCOUNT_TYPE)

    expires = DateTimeField(
        "Zniżka wygasa",
        null=True,
        blank=True,
        help_text="Jeżeli nie ustawiono znaczy, że nie wygasa.",
    )

    class Meta:
        verbose_name = "Kod promocyjny"
        verbose_name_plural = "Kody promocyjne"

    def __str__(self) -> str:
        return f"{self.discount_code}"


class DiscountApplicationApplied(Model):
    """Represents discounts applied to applications"""

    application = ForeignKey(
        "WebinarApplication", verbose_name="Zgłoszenie", on_delete=CASCADE
    )

    discount_weight = PositiveSmallIntegerField(
        "Waga rabatu",
        default=1,
        help_text="Pole używane do ograniczenia liczby nałożonych rabatów",
    )

    discount_code = ForeignKey(
        "DiscountCode",
        verbose_name="Kod promocyjny",
        on_delete=RESTRICT,
        null=True,
        blank=True,
    )

    amount = SmallIntegerField("Wartość zniżki (zł)")

    name = CharField("Krótka nazwa", max_length=64)

    description = CharField("Krótki opis", max_length=150, blank=True)

    class Meta:
        verbose_name = "Zniżka (zgłoszenie)"
        verbose_name_plural = "Zniżka (zgłoszenia)"

    def __str__(self) -> str:
        return f"{self.id}"  # type: ignore
