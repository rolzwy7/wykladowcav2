"""
Webinar application model
"""

# flake8: noqa=E501
# pylint: disable=line-too-long

import uuid

from django.conf import settings
from django.db.models import (
    CASCADE,
    RESTRICT,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ForeignKey,
    Manager,
    Model,
    OneToOneField,
    PositiveSmallIntegerField,
    Q,
    QuerySet,
    TextField,
    UUIDField,
)

from core.consts import CHOICES_VAT_EXEMPTIONS, VAT_EXEMPTION_0, VAT_VALUE_PERCENT
from core.libs.normalizers import normalize_phone_number
from core.libs.validators import validate_nip_modelfield

from .enums import ApplicationStatus, InvoiceType, WebinarApplicationType
from .webinar_model import Webinar


class WebinarApplicationManager(Manager):
    """WebinarApplication query Manager"""

    def sent_applications_for_webinar(
        self, webinar: Webinar
    ) -> QuerySet["WebinarApplication"]:
        """Get sent applications"""
        return self.get_queryset().filter(
            # for given webinar
            Q(webinar=webinar)
            # with sent status
            & Q(status=ApplicationStatus.SENT)
        )

    def unfinished_applications_for_webinar(
        self, webinar: Webinar
    ) -> QuerySet["WebinarApplication"]:
        """Get unfinished applications"""
        return self.get_queryset().filter(
            # for given webinar
            Q(webinar=webinar)
            # with init status
            & Q(status=ApplicationStatus.INIT)
        )

    def resigned_applications_for_webinar(
        self, webinar: Webinar
    ) -> QuerySet["WebinarApplication"]:
        """Get resigned applications"""
        return self.get_queryset().filter(
            # for given webinar
            Q(webinar=webinar)
            # with resignation status
            & Q(status=ApplicationStatus.RESIGNATION)
        )


class WebinarApplicationCompany(Model):
    """Represents application company (buyer or recipient)"""

    nip = CharField("NIP", max_length=32, validators=[validate_nip_modelfield])
    name = CharField("Nazwa", max_length=250)
    address = CharField("Adres", max_length=150)
    postal_code = CharField("Kod pocztowy", max_length=16)
    city = CharField("Miejscowość", max_length=150)
    email = EmailField("Email", blank=True)
    phone_number = CharField("Telefon", max_length=150, blank=True)

    def __str__(self):
        return f"{self.nip} - {self.name}"


class WebinarApplicationSubmitter(Model):
    """Represents application submitter"""

    is_participant = BooleanField("Jest też uczestnikiem", default=False)
    first_name = CharField("Imię", max_length=100, blank=True)
    last_name = CharField("Nazwisko", max_length=100, blank=True)
    email = EmailField("Email")
    phone = CharField("Numer telefonu", max_length=100)

    def __str__(self):
        return f"{self.fullname}"

    def save(self, *args, **kwargs) -> None:
        self.phone = normalize_phone_number(self.phone)
        return super().save(*args, **kwargs)

    @property
    def fullname(self):
        """Returns submitter's fullname"""
        return f"{self.first_name} {self.last_name}"


class WebinarApplicationPrivatePerson(Model):
    """Represents application private person"""

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


class WebinarApplicationInvoice(Model):
    """Represents application invoice"""

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


class WebinarApplicationTracking(Model):
    """WebinarApplicationTracking"""

    created_at = DateTimeField("Stworzono", auto_now_add=True)

    webinar = ForeignKey("Webinar", on_delete=CASCADE, verbose_name="Webinar")

    tracking_code = CharField("Kod śledzący", max_length=64)

    campaign_id = CharField("ID kampanii mailingowej", max_length=32, blank=True)


class WebinarApplication(Model):
    """Webinar Application Model"""

    APPLICATION_TYPE = [
        (WebinarApplicationType.COMPANY, "Firma"),
        (WebinarApplicationType.JSFP, "JSFP"),
        (WebinarApplicationType.PRIVATE_PERSON, "Osoba prywatna"),
    ]

    STATUS = [
        (ApplicationStatus.INIT, "Zgłoszenie rozpoczęte"),
        (ApplicationStatus.SENT, "Zgłoszenie wysłane"),
        (ApplicationStatus.RESIGNATION, "Rezygnacja ze zgłoszenia"),
        (ApplicationStatus.PAYED, "Faktura opłacona"),
    ]

    manager = WebinarApplicationManager()

    status = CharField(max_length=32, default=ApplicationStatus.INIT, choices=STATUS)

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
    webinar = ForeignKey("Webinar", on_delete=CASCADE, verbose_name="Webinar")

    # Buyer
    buyer = OneToOneField(
        "WebinarApplicationCompany",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="application_buyer",
        verbose_name="Nabywca",
    )

    # Recipient
    recipient = OneToOneField(
        "WebinarApplicationCompany",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="application_recipient",
        verbose_name="Odbiorca",
    )

    private_person = OneToOneField(
        "WebinarApplicationPrivatePerson",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="application_private_person",
        verbose_name="Osoba prywatna",
    )

    # Invoice
    invoice = OneToOneField(
        "WebinarApplicationInvoice",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="application_invoice",
        verbose_name="Faktura",
    )

    # Submitter
    submitter = OneToOneField(
        "WebinarApplicationSubmitter",
        on_delete=CASCADE,
        blank=True,
        null=True,
        related_name="application_submitter",
        verbose_name="Osoba zgłaszająca",
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

    step_buyer_finished = BooleanField(
        "Krok Nabywca zrealizowany",
        default=False,
        help_text="Czy zgłaszający wysłał formularz z nabywcą?",
    )

    step_recipient_finished = BooleanField(
        "Krok Odbiorca zrealizowany",
        default=False,
        help_text="Czy zgłaszający wysłał formularz z odbiorcą?",
    )

    step_participants_finished = BooleanField(
        "Krok Uczestnicy zrealizowany",
        default=False,
        help_text="Czy zgłaszający wysłał formularz z uczestnikami?",
    )

    step_invoice_finished = BooleanField(
        "Krok Faktura zrealizowany",
        default=False,
        help_text="Czy zgłaszający wysłał formularz z fakturą?",
    )

    got_to_summary = BooleanField(
        "Dotarł do podsumowania",
        default=False,
        help_text="Czy zgłaszający dotarł do strony podsumowania?",
    )

    step_dt_buyer_end = DateTimeField("buyer_end", blank=True, null=True)

    step_dt_recipient_start = DateTimeField("recipient_start", blank=True, null=True)
    step_dt_recipient_end = DateTimeField("recipient_end", blank=True, null=True)

    step_dt_participants_start = DateTimeField(
        "participants_start", blank=True, null=True
    )
    step_dt_participants_end = DateTimeField("participants_end", blank=True, null=True)

    step_dt_invoice_start = DateTimeField("invoice_start", blank=True, null=True)
    step_dt_invoice_end = DateTimeField("invoice_end", blank=True, null=True)

    step_dt_summary_start = DateTimeField("summary_start", blank=True, null=True)
    step_dt_summary_end = DateTimeField("summary_end", blank=True, null=True)

    recording_dt = DateTimeField("Początek dostępu do nagrania", blank=True, null=True)

    fake_application = BooleanField(
        "Fałszywe zgłoszenie",
        default=False,
        help_text="Czy prawdopodobnie fałszywe zgłoszenie?",
    )
    fake_application_logs = TextField(
        "Fałszywe zgłoszenie (logi)",
        blank=True,
        help_text="Logi detektora fałszywych zgłoszeń",
    )

    spy_object = ForeignKey(
        "SpyObject",
        on_delete=RESTRICT,
        null=True,
        blank=True,
        verbose_name="Spy Object",
    )

    class Meta:
        """meta"""

        verbose_name = "Zgłoszenie"
        verbose_name_plural = "Zgłoszenia"

    def __str__(self) -> str:
        return f"Zgłoszenie {self.id}"  # type: ignore # pylint: disable=no-member

    @property
    def metadata(self):
        """metadata"""
        return WebinarApplicationMetadata.objects.filter(application=self).first()

    @property
    def price_brutto(self):
        """Calculate BRUTTO price for one participant"""

        # If not VAT exempt apply `VAT_VALUE_PERCENT` value of VAT
        if not self.invoice.is_vat_exempt:  # type: ignore # pylint: disable=no-member
            multiplier = round((100 + VAT_VALUE_PERCENT) / 100, 2)
            return round(self.price_netto * multiplier, 2)

        return self.price_netto  # is VAT exempt


class WebinarApplicationMetadata(Model):
    """Metadata for Webinar Application"""

    application = ForeignKey("WebinarApplication", on_delete=CASCADE)

    phoned = BooleanField(default=False)

    invoice_id = CharField(max_length=32, blank=True)
    invoice_number = CharField(max_length=64, blank=True)
    invoice_url = CharField(max_length=300, blank=True)

    terms_accepted = BooleanField("Zaakceptowano regulamin", default=False)

    ip_address = CharField(max_length=64, blank=True)

    vat_status = CharField(max_length=64, blank=True)

    def __str__(self) -> str:
        return f"Zgłoszenie {self.application.id} metadata"  # pylint: disable=no-member
