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
    Q,
    QuerySet,
    TextField,
    UUIDField,
)

from core.consts import (
    CHOICES_VAT_EXEMPTIONS,
    VAT_EXEMPTION_0,
    VAT_VALUE_PERCENT,
    WE_ARE_TAX_EXEMPT,
)
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
        return str(self.nip)


class WebinarApplicationSubmitter(Model):
    """Represents application submitter"""

    is_participant = BooleanField("Jest też uczestnikiem", default=False)
    first_name = CharField("Imię", max_length=100, blank=True)
    last_name = CharField("Nazwisko", max_length=100, blank=True)
    email = EmailField("Email")
    phone = CharField("Numer telefonu", max_length=100)

    def __str__(self):
        return f"{self.fullname}"

    @property
    def fullname(self):
        """Returns submitter's fullname"""
        return f"{self.first_name} {self.last_name}"


class WebinarApplicationPrivatePerson(Model):
    """Represents application submitter"""

    first_name = CharField("Imię", max_length=100)
    last_name = CharField("Nazwisko", max_length=100)

    address = CharField("Adres", max_length=150)
    postal_code = CharField("Kod pocztowy", max_length=16)
    city = CharField("Miejscowość", max_length=150)

    email = EmailField("Email")
    phone = CharField("Numer telefonu", max_length=100)

    def __str__(self):
        return f"{self.fullname}"

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
        "Dodatkowe informacje (Faktura)", max_length=200, blank=True
    )

    # Vat exemption
    vat_exemption = CharField(
        "Zwolnienie z VAT",
        max_length=64,
        choices=CHOICES_VAT_EXEMPTIONS,
        default=VAT_EXEMPTION_0.db_key,
    )

    def __str__(self):
        return f"{self.invoice_email}"


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

    status = CharField(
        max_length=32, default=ApplicationStatus.INIT, choices=STATUS
    )

    created_at = DateTimeField("Stworzono", auto_now_add=True)
    uuid = UUIDField(
        "Identyfikator zgłoszenia", default=uuid.uuid4, unique=True
    )

    refcode = CharField("Kod referencyjny", max_length=32, blank=True)

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

    class Meta:
        verbose_name = "Zgłoszenie"
        verbose_name_plural = "Zgłoszenia"

    def __str__(self) -> str:
        return f"Zgłoszenie {self.id}"  # type: ignore

    # @property  # TODO: move to service
    # def participants(self) -> QuerySet["WebinarParticipant"]:
    #     """Return paticipants for this application"""
    #     return (
    #         WebinarParticipant.manager.get_valid_participants_for_application(
    #             application=self
    #         )
    #     )

    # @property  # TODO: move to service
    # def total_price_netto(self):
    #     """Calculate total NETTO price for this application"""
    #     return self.participants.count() * self.price_netto

    @property
    def price_brutto(self):
        """Calculate BRUTTO price for one participant"""

        # Take exemption into consideration
        if WE_ARE_TAX_EXEMPT:
            return self.price_netto

        # Application is not VAT exempt
        if self.invoice.vat_exemption != VAT_EXEMPTION_0.db_key:  # type: ignore
            return self.price_netto

        multiplier = round((100 + VAT_VALUE_PERCENT) / 100, 2)
        return round(self.price_netto * multiplier, 2)


class WebinarApplicationMetadata(Model):
    """Metadata for Webinar Application"""

    application = ForeignKey("WebinarApplication", on_delete=CASCADE)

    phoned = BooleanField(default=False)

    invoice_id = CharField(max_length=32, blank=True)
    invoice_number = CharField(max_length=64, blank=True)
    invoice_url = CharField(max_length=300, blank=True)

    terms_accepted = BooleanField("Zaakceptowano regulamin", default=False)

    ip_address = CharField(max_length=64, blank=True)

    def __str__(self) -> str:
        return f"Zgłoszenie {self.application.id} metadata"
