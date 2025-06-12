"""Spy Object Model"""

# flake8: noqa=E501

import uuid

from django.db.models import BooleanField, CharField, DateTimeField, Model, UUIDField


class SpyObject(Model):
    """Spy Object"""

    created_at = DateTimeField(auto_now_add=True)

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Params
    SOURCE = [
        ("YES", "TAK"),
        ("NO", "NIE"),
    ]

    source = CharField(
        "Źródło",
        max_length=32,
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

    class Meta:
        ordering = ["-created_at"]
