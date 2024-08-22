from django.db.models import (
    BooleanField,
    CharField,
    EmailField,
    FileField,
    Manager,
    Model,
    TextField,
)

from core.libs.validators import validate_nip_modelfield


class OfferContactManager(Manager):
    """OfferContact query Manager"""

    ...


class OfferContact(Model):
    """OfferContact"""

    manager = OfferContactManager()

    # created at
    # updated at

    offer_name = CharField("Nazwa", max_length=64)

    nip = CharField("NIP", max_length=32, validators=[validate_nip_modelfield])
    name = CharField("Nazwa", max_length=250)
    address = CharField("Adres", max_length=150)
    postal_code = CharField("Kod pocztowy", max_length=16)
    city = CharField("Miejscowość", max_length=150)

    first_name = CharField("Imię", max_length=100)
    last_name = CharField("Nazwisko", max_length=100)
    email_contact = EmailField("Email kontaktowy")
    phone = CharField("Numer telefonu", max_length=50)
    email_confirmation = EmailField("Email potwierdzenie")

    file = FileField("Plik", upload_to="uploads/offer_contact")

    additional_info = TextField("Uwagi", max_length=250, blank=True)

    accepted_rodo = BooleanField("Zaakceptowano RODO")
    accepted_terms = BooleanField("Zaakceptowano Regulamin")

    class Meta:
        verbose_name = "Oferta Kontakt"
        verbose_name_plural = "Oferty Kontaky"
