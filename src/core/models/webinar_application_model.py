import uuid

from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ForeignKey,
    Model,
    PositiveSmallIntegerField,
    TextField,
    UUIDField,
)

from core.consts import CHOICES_VAT_EXEMPTIONS, VAT_EXEMPTION_0

from .enums import ApplicationStatus, InvoiceType, WebinarApplicationType


class WebinarApplicationCompany(Model):
    nip = CharField("NIP", max_length=32)
    name = CharField("Nazwa", max_length=250)
    address = CharField("Adres", max_length=150)
    postal_code = CharField("Kod pocztowy", max_length=16)
    city = CharField("Miasto", max_length=150)
    email = CharField("Email", max_length=150, blank=True)
    phone_number = CharField("Telefon", max_length=150, blank=True)


class WebinarApplicationSubmitter(Model):
    is_participant = BooleanField("Jest też uczestnikiem", default=False)
    first_name = CharField("Imię", max_length=100)
    last_name = CharField("Nazwisko", max_length=100)
    email = CharField("E-mail", max_length=100)
    phone = CharField("Numer telefonu", max_length=100)


class WebinarApplication(Model):
    class Meta:
        verbose_name = "Zgłoszenie"
        verbose_name_plural = "Zgłoszenia"

    APPLICATION_TYPE = [
        (WebinarApplicationType.COMPANY, "Firma"),
        (WebinarApplicationType.JSFP, "Firma (Nabywca / Odbiorca)"),
        (WebinarApplicationType.PRIVATE_PERSON, "Osoba prywatna"),
    ]

    STATUS = [
        (ApplicationStatus.INIT, "Zgłoszenie rozpoczęte"),
        (ApplicationStatus.SENT, "Zgłoszenie wysłane"),
    ]

    status = CharField(
        max_length=32, default=ApplicationStatus.INIT, choices=STATUS
    )

    created_at = DateTimeField("Stworzono", auto_now_add=True)
    uuid = UUIDField(
        "Identyfikator zgłoszenia", default=uuid.uuid4, unique=True
    )

    # Price
    discount_applied = BooleanField("Promocja nałożona", default=False)
    price_netto = PositiveSmallIntegerField("Cena NETTO")

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
    buyer = ForeignKey(
        "WebinarApplicationCompany",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="application_buyer",
        verbose_name="Nabywca",
    )

    # Receiver
    receiver = ForeignKey(
        "WebinarApplicationCompany",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="application_receiver",
        verbose_name="Odbiorca",
    )

    # Invoice
    INVOICE_TYPE = [
        (InvoiceType.INVOICE_DIGITAL, "Faktura elektroniczna"),
        (InvoiceType.INVOICE_PAPER, "Faktura papierowa"),
    ]

    invoice_type = CharField(
        "Typ faktury",
        max_length=64,
        choices=INVOICE_TYPE,
        default=InvoiceType.INVOICE_DIGITAL,
    )
    invoice_email = EmailField(
        "E-mail (Faktura)",
        blank=True,
        help_text="E-mail na który zostanie przesłana faktura",
    )
    invoice_additional_info = TextField(
        "Dodatkowe informacje (Faktura)", max_length=200, blank=True
    )

    # Vat exemption
    vat_exemption = CharField(
        "Zwolnienie z VAT",
        max_length=64,
        choices=CHOICES_VAT_EXEMPTIONS,
        default=VAT_EXEMPTION_0.db_key,
    )

    # Submitter
    submitter = ForeignKey(
        "WebinarApplicationSubmitter",
        on_delete=CASCADE,
        blank=True,
        null=True,
        related_name="application_submitter",
        verbose_name="Osoba zgłaszająca",
    )

    # Additional Information
    additional_information = TextField("Uwagi", blank=True)


class WebinarApplicationMetadata(Model):
    application = ForeignKey("WebinarApplication", on_delete=CASCADE)

    phoned = BooleanField(default=False)
