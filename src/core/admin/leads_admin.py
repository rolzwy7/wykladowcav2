# flake8: noqa

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from core.models import LeadModel


@admin.register(LeadModel)
class LeadModelAdmin(ModelAdmin):
    list_display = [
        "__str__",
        "is_subscribed",
        "was_activated",
        "lead_source",
        "singup_ip_address",
    ]
