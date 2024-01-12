"""
Conference admin
"""

from django.contrib import admin
from django.contrib.admin import ModelAdmin, register

from core.models import (
    ConferenceCycle,
    ConferenceEdition,
    ConferenceFreeParticipant,
    ConferenceSchedule,
)

admin.site.register(ConferenceEdition)
admin.site.register(ConferenceCycle)
admin.site.register(ConferenceSchedule)


@register(ConferenceFreeParticipant)
class ConferenceFreeParticipantModelAdmin(ModelAdmin):
    """ConferenceFreeParticipant"""

    list_display = [
        "email",
        "edition",
        "first_name",
        "last_name",
        "voivodeship",
        "phone",
        "know_from",
        "using_closed_webinars",
    ]

    search_fields = ["first_name", "last_name", "email", "phone"]

    list_filter = [
        "voivodeship",
        "know_from",
        "using_closed_webinars",
    ]
