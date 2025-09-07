"""Spy Object Model"""

# flake8: noqa=E501

import uuid

from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    FloatField,
    Model,
    UUIDField,
)


class SpyObject(Model):
    """Spy Object"""

    created_at = DateTimeField(auto_now_add=True)

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Params
    SOURCE = [
        ("WEBINAR_SEE_MORE", "Klik: Webinar przycisk zobacz więcej"),
        ("VISITED_CLOSED_WEBINAR_PAGE", "Wejście: Strona szkolenie zamknięte"),
        (
            "AGGREGATE_NO_WEBINARS_CLICK_SHOW_FORM",
            "Klik: Przycisk Zapisz się Brak Terminów",
        ),
        ("AGGREGATE_NO_WEBINARS_FORM_SUBMIT", "Formularz: Brak terminów Przypomnij"),
        ("WEBINAR_APPLICATION", "Formularz: Zgłoszenie webinar"),
        ("ADVERT_POPUP_CLICK", "Advert popup"),
    ]

    source = CharField(
        "Źródło",
        max_length=64,
        choices=SOURCE,
    )

    param_a = CharField(max_length=64, blank=True)
    param_b = CharField(max_length=64, blank=True)
    param_c = CharField(max_length=64, blank=True)

    # Tracking id
    ip_address = CharField(max_length=64, blank=True)
    session_key = CharField(max_length=64, blank=True)
    tracking_code = CharField("Kod śledzący", max_length=32, blank=True)
    campaign_id = CharField("ID kampanii mailingowej", max_length=32, blank=True)
    fingerprint = CharField(max_length=128, blank=True)
    user_agent = CharField(max_length=128, blank=True)
    logged_in = BooleanField("Zalogowany?", default=False)
    user_id = CharField(max_length=16, blank=True)

    google_recaptcha_v3 = FloatField("Google reCAPTCHA v3", default=-1.0)

    class Meta:
        ordering = ["-created_at"]
