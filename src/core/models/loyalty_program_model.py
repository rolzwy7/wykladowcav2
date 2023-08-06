from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    DecimalField,
    FileField,
    ForeignKey,
    Manager,
    Model,
    OneToOneField,
    PositiveSmallIntegerField,
    TextField,
)

from .enums import LoyaltyProgramIncomeStatus, LoyaltyProgramPayoutStatus


class LoyaltyProgramManager(Manager):
    """LoyaltyProgram query Manager"""

    ...


class LoyaltyProgram(Model):
    """Represents loyalty program user details"""

    manager = LoyaltyProgramManager()

    created_at = DateTimeField(auto_now_add=True)

    ref_number = CharField(max_length=32, primary_key=True)

    user = OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        verbose_name="Użytkownik",
    )

    provision_percent = PositiveSmallIntegerField("Prowizja (%)", default=10)

    class Meta:
        verbose_name = "Program partnerski (Użytkownik)"
        verbose_name_plural = "Program partnerski (Użytkownicy)"

    def __str__(self) -> str:
        return f"{self.ref_number}"


class LoyaltyProgramIncome(Model):
    """Represents loyalty program income"""

    created_at = DateTimeField(auto_now_add=True)

    loyalty_program = ForeignKey(
        "LoyaltyProgram", verbose_name="Kod referencyjny", on_delete=CASCADE
    )

    application = ForeignKey(
        "WebinarApplication", verbose_name="Zgłoszenie", on_delete=CASCADE
    )

    INCOME_STATUS = [
        (LoyaltyProgramIncomeStatus.PROCESSING, "W trakcie przetwarzania"),
        (LoyaltyProgramIncomeStatus.PAYABLE, "Do wypłaty"),
        (LoyaltyProgramIncomeStatus.VIOLATING, "Niezgodne z regulaminem"),
    ]

    status = CharField(
        "Status należności",
        max_length=32,
        choices=INCOME_STATUS,
        default=LoyaltyProgramIncomeStatus.PROCESSING,
    )

    note_employee = TextField("Uwagi do należności (pracownik)", blank=True)

    amount_brutto = DecimalField(
        "Wartość Brutto", max_digits=10, decimal_places=2
    )

    class Meta:
        verbose_name = "Program partnerski (Należność)"
        verbose_name_plural = "Program partnerski (Należności)"

    def __str__(self) -> str:
        return f"{self.id}"  # type: ignore


class LoyaltyProgramPayout(Model):
    """Represents loyalty program payout"""

    created_at = DateTimeField(auto_now_add=True)

    loyalty_program = ForeignKey(
        "LoyaltyProgram", verbose_name="Kod referencyjny", on_delete=CASCADE
    )

    PAYOUT_STATUS = [
        (
            LoyaltyProgramPayoutStatus.WAITING_FOR_CONFIRMATION,
            "Czeka na potwierdzenie",
        ),
        (LoyaltyProgramPayoutStatus.PAYED, "Zapłacono"),
        (LoyaltyProgramPayoutStatus.REFUSED, "Odmówiono zapłaty"),
    ]

    status = CharField(
        "Status należności",
        max_length=32,
        choices=PAYOUT_STATUS,
        default=LoyaltyProgramPayoutStatus.WAITING_FOR_CONFIRMATION,
    )

    note_employee = TextField("Uwagi do wypłaty (pracownik)", blank=True)

    payout_brutto = DecimalField(
        "Wartość Brutto", max_digits=10, decimal_places=2
    )

    invoice_attachment = FileField()

    class Meta:
        verbose_name = "Program partnerski (Wypłata)"
        verbose_name_plural = "Program partnerski (Wypłaty)"

    def __str__(self) -> str:
        return f"{self.id}"  # type: ignore
