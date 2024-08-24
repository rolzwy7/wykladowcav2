"""Service Offer Model"""

# flake8: noqa

from django.db.models import (
    RESTRICT,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    FileField,
    ForeignKey,
    Manager,
    Model,
    SlugField,
    TextField,
)

from core.libs.validators import validate_nip_modelfield
from core.models.enums import ServiceOfferApplicationStatus


class ServiceOfferManager(Manager):
    """ServiceOffer query Manager"""

    ...


class ServiceOffer(Model):
    """ServiceOffer"""

    manager = ServiceOfferManager()

    created_at = DateTimeField("Stworzono", auto_now_add=True)

    slug = SlugField(
        "Skrót URL",
        max_length=150,
        unique=True,
        help_text="Slug",
    )

    category = ForeignKey("WebinarCategory", on_delete=RESTRICT)

    offer_title = CharField("Nazwa oferty", max_length=250)
    short_name = CharField("Krótka Nazwa", max_length=100)
    description_primary_html = TextField(
        "DESCRIPTION PRIMARY", default="[DESCRIPTION_PRIMARY]"
    )
    steps_html = TextField("STEPS_HTML", default="[STEPS_HTML]")
    call_to_action_html = TextField("CTA_HTML", default="[CALL_TO_ACTION_HTML]")
    button_html = TextField("BUTTON_HTML", default="[BUTTON_HTML]")

    nip_place_text = TextField("NIP_PLACE_TEXT", default="[NIP_PLACE_TEXT]")
    name_place_text = TextField("NAME_PLACE_TEXT", default="[NAME_PLACE_TEXT]")
    file_text = TextField("FILE_TEXT", default="[FILE_TEXT]")

    thanks_title_text = TextField("THANKS_TITLE_TEXT", default="[THANKS_TITLE_TEXT]")
    thanks_html = TextField("THANKS_HTML", default="[THANKS_HTML]")

    class Meta:
        verbose_name = "Oferta Usługi"
        verbose_name_plural = "Oferty Usług"


class ServiceOfferApplicationManager(Manager):
    """ServiceOfferApplication query Manager"""

    ...


class ServiceOfferApplication(Model):
    """ServiceOfferApplication"""

    manager = ServiceOfferApplicationManager()

    created_at = DateTimeField("Stworzono", auto_now_add=True)

    service_offer = ForeignKey("ServiceOffer", on_delete=RESTRICT)

    STATUS = (
        (ServiceOfferApplicationStatus.SENT, "Wysłano zgłoszenie"),
        (ServiceOfferApplicationStatus.OFFER, "Przygotowano ofertę"),
        (ServiceOfferApplicationStatus.ACCEPTED, "Klient zaakceptował ofertę"),
        (ServiceOfferApplicationStatus.REJECTED, "Klient odrzucił ofertę"),
        (ServiceOfferApplicationStatus.PAID, "Zapłacono za usługę"),
        (ServiceOfferApplicationStatus.UNPAID, "Nie zapłacono za usługę"),
    )
    status = CharField(
        max_length=32, choices=STATUS, default=ServiceOfferApplicationStatus.SENT
    )

    nip = CharField(
        "NIP",
        max_length=32,
        validators=[validate_nip_modelfield],
    )
    name = CharField("Nazwa", max_length=250)
    address = CharField("Adres", max_length=150)
    postal_code = CharField("Kod pocztowy", max_length=16)
    city = CharField("Miejscowość", max_length=150)

    first_name = CharField("Imię", max_length=100)
    last_name = CharField("Nazwisko", max_length=100)
    email_contact = EmailField("Email kontaktowy")
    email_confirmation = EmailField("Email potwierdzenie", blank=True)
    phone = CharField("Numer telefonu", max_length=50)

    file = FileField("Plik", upload_to="uploads/offer_contact", null=True, blank=True)

    additional_info = TextField("Uwagi", max_length=250, blank=True)

    accepted_rodo = BooleanField("Zaakceptowano RODO")
    accepted_terms = BooleanField("Zaakceptowano Regulamin")

    tracking_code = CharField("Kod śledzący", max_length=32, blank=True)

    sent_at = DateTimeField(null=True)
    sent_ip_address = CharField(max_length=64, blank=True)

    accepted_at = DateTimeField(null=True)
    accepted_ip_address = CharField(max_length=64, blank=True)

    class Meta:
        verbose_name = "Oferta Usługi - Zgłoszenie"
        verbose_name_plural = "Oferty Usług - Zgłoszenia"


class ServiceOfferLeadManager(Manager):
    """ServiceOfferLead query Manager"""

    ...


class ServiceOfferLead(Model):
    """ServiceOfferLead"""

    manager = ServiceOfferLeadManager()

    created_at = DateTimeField("Stworzono", auto_now_add=True)

    service_offer = ForeignKey("ServiceOffer", on_delete=RESTRICT)

    tracking_code = CharField("Kod śledzący", max_length=32, blank=True)
    email = EmailField("Email", blank=True)

    class Meta:
        verbose_name = "Oferta Usługi - Leady"
        verbose_name_plural = "Oferty Usług - Leady"
