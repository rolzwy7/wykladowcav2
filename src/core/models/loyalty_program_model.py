from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    OneToOneField,
    Q,
    QuerySet,
    TextField,
)
from django.utils.timezone import now


class LoyaltyProgramManager(Manager):
    """Eventlog query Manager"""

    ...


class LoyaltyProgram(Model):
    """Represents loyality program user details"""

    manager = LoyaltyProgramManager()

    created_at = DateTimeField(auto_now_add=True)

    ref_number = CharField(max_length=32, primary_key=True)  # TODO: Validation

    user = OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        verbose_name="Użytkownik",
    )

    class Meta:
        verbose_name = "Program partnerski (Użytkownik)"
        verbose_name_plural = "Program partnerski (Użytkownicy)"

    def __str__(self) -> str:
        return f"{self.ref_number}"


class LoyaltyProgramIncome(Model):
    """Represents loyality program income"""

    created_at = DateTimeField(auto_now_add=True)

    fk: LoyaltyProgram

    fk: Application

    status = ...  # realizacja, odmowiono, zrealizowano

    amount = ...  # integer, brutto, netto ???

    class Meta:
        verbose_name = "Program partnerski (Należność)"
        verbose_name_plural = "Program partnerski (Należności)"


class LoyaltyProgramPayout(Model):
    """Represents loyality program payout"""

    created_at = DateTimeField(auto_now_add=True)

    fk: LoyaltyProgram

    status = ...  # realizacja, odmowiono, zrealizowano

    amount = ...  # integer, brutto, netto ???

    invoice_attachment = ...  # file

    class Meta:
        verbose_name = "Program partnerski (Wypłata)"
        verbose_name_plural = "Program partnerski (Wypłaty)"
