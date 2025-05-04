"""
Webinar application model
"""

# flake8: noqa=E501
# pylint: disable=line-too-long

import uuid

from django.conf import settings
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ForeignKey,
    Manager,
    Model,
    OneToOneField,
    PositiveSmallIntegerField,
    TextField,
    UUIDField,
)

from core.consts import CHOICES_VAT_EXEMPTIONS, VAT_EXEMPTION_0, VAT_VALUE_PERCENT
from core.libs.normalizers import normalize_phone_number
from core.libs.validators import validate_nip_modelfield

from .enums import InvoiceType, SaleRecordingApplicationStatus, WebinarApplicationType


class SaleRecordingApplicationManager(Manager):
    """SaleRecordingApplicationManager"""

    ...


class SaleRecordingApplicationCompany(Model):
    """SaleRecordingApplicationCompany"""

    nip = CharField("NIP", max_length=32, validators=[validate_nip_modelfield])
    name = CharField("Nazwa", max_length=250)
    address = CharField("Adres", max_length=150)
    postal_code = CharField("Kod pocztowy", max_length=16)
    city = CharField("Miejscowość", max_length=150)
    email = EmailField("Email", blank=True)
    phone_number = CharField("Telefon", max_length=150, blank=True)

    def __str__(self):
        return f"{self.nip} - {self.name}"


class SaleRecordingApplicationPrivatePerson(Model):
    """SaleRecordingApplicationPrivatePerson"""

    first_name = CharField("Imię", max_length=100)
    last_name = CharField("Nazwisko", max_length=100)

    address = CharField("Adres", max_length=150)
    postal_code = CharField("Kod pocztowy", max_length=16)
    city = CharField("Miejscowość", max_length=150)

    email = EmailField("Email")
    phone = CharField("Numer telefonu", max_length=100)

    def __str__(self):
        return f"{self.fullname} <{self.email}>"

    def save(self, *args, **kwargs) -> None:
        self.phone = normalize_phone_number(self.phone)
        return super().save(*args, **kwargs)

    @property
    def fullname(self):
        """Returns submitter's fullname"""
        return f"{self.first_name} {self.last_name}"


class SaleRecordingApplicationInvoice(Model):
    """SaleRecordingApplicationInvoice"""

    INVOICE_TYPE = [
        (InvoiceType.INVOICE_DIGITAL, "Faktura elektroniczna"),
        (InvoiceType.INVOICE_PAPER, "Faktura elektroniczna i papierowa"),
    ]

    invoice_type = CharField(
        "Typ faktury",
        max_length=64,
        choices=INVOICE_TYPE,
        default=InvoiceType.INVOICE_DIGITAL,
    )
    invoice_email = EmailField(
        "E-mail (Faktura)",
        help_text="E-mail na który zostanie przesłana faktura",
    )
    invoice_additional_info = TextField(
        "Dodatkowe informacje widoczne na Fakturze", max_length=200, blank=True
    )

    # Vat exemption
    vat_exemption = CharField(
        "Zwolnienie z VAT",
        max_length=64,
        choices=CHOICES_VAT_EXEMPTIONS,
        default=VAT_EXEMPTION_0.db_key,
    )

    @property
    def is_vat_exempt(self) -> bool:
        """Check if invoice is VAT exempt"""
        return self.vat_exemption != VAT_EXEMPTION_0.db_key

    def __str__(self):
        return f"{self.invoice_email}"


class SaleRecordingApplication(Model):
    """Webinar Application Model"""

    APPLICATION_TYPE = [
        (WebinarApplicationType.COMPANY, "Firma"),
        (WebinarApplicationType.JSFP, "JSFP"),
        (WebinarApplicationType.PRIVATE_PERSON, "Osoba prywatna"),
    ]

    STATUS = [
        (SaleRecordingApplicationStatus.INIT, "Rozpoczęto zakup nagrania"),
        (SaleRecordingApplicationStatus.CANCELED_BY_SYSTEM, "System anulował zakup"),
        (
            SaleRecordingApplicationStatus.WAITING_FOR_PAYMENT,
            "Stworzono zamówienie, czekam na płatność",
        ),
        (SaleRecordingApplicationStatus.PAYED, "Opłacono zamówienie"),
    ]

    manager = SaleRecordingApplicationManager()

    status = CharField(
        max_length=32, default=SaleRecordingApplicationStatus.INIT, choices=STATUS
    )

    created_at = DateTimeField("Stworzono", auto_now_add=True)
    uuid = UUIDField("Identyfikator zgłoszenia", default=uuid.uuid4, unique=True)

    refcode = CharField("Kod referencyjny", max_length=32, blank=True)
    tracking_code = CharField("Kod śledzący", max_length=32, blank=True)
    campaign_id = CharField("ID kampanii mailingowej", max_length=32, blank=True)

    # Price
    price_netto = PositiveSmallIntegerField("Cena NETTO")
    price_old = PositiveSmallIntegerField("Stara cena", null=True)

    # Application Type
    application_type = CharField(
        "Typ zgłoszenia",
        max_length=64,
        choices=APPLICATION_TYPE,
        default=WebinarApplicationType.COMPANY,
    )

    # Webinar
    sale_recording = ForeignKey(
        "SaleRecording", on_delete=CASCADE, verbose_name="SaleRecording"
    )

    # Buyer
    buyer = OneToOneField(
        "SaleRecordingApplicationCompany",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="application_buyer",
        verbose_name="Nabywca",
    )

    # Recipient
    recipient = OneToOneField(
        "SaleRecordingApplicationCompany",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="application_recipient",
        verbose_name="Odbiorca",
    )

    private_person = OneToOneField(
        "SaleRecordingApplicationPrivatePerson",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="application_private_person",
        verbose_name="Osoba prywatna",
    )

    # Invoice
    invoice = OneToOneField(
        "SaleRecordingApplicationInvoice",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="application_invoice",
        verbose_name="Faktura",
    )

    # Additional Information
    additional_information = TextField("Uwagi", blank=True)

    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name="Użytkownik",
    )

    fakturownia_invoice_id = CharField(max_length=32, blank=True)
    fakturownia_invoice_number = CharField(max_length=64, blank=True)
    fakturownia_invoice_url = CharField(max_length=300, blank=True)

    terms_accepted = BooleanField("Zaakceptowano regulamin", default=False)

    ip_address = CharField(max_length=64, blank=True)

    class Meta:
        """meta"""

        verbose_name = "Zgłoszenie (nagranie na sprzedaż)"
        verbose_name_plural = "Zgłoszenia (nagranie na sprzedaż)"

    def __str__(self) -> str:
        return f"Zgłoszenie nagranie na sprzedaż {self.id}"  # type: ignore # pylint: disable=no-member

    @property
    def price_brutto(self):
        """Calculate BRUTTO price for one participant"""

        # If not VAT exempt apply `VAT_VALUE_PERCENT` value of VAT
        if not self.invoice.is_vat_exempt:  # type: ignore # pylint: disable=no-member
            multiplier = round((100 + VAT_VALUE_PERCENT) / 100, 2)
            return round(self.price_netto * multiplier, 2)

        return self.price_netto  # is VAT exempt
