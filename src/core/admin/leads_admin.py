# flake8: noqa

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from core.models import LeadModel


@admin.register(LeadModel)
class LeadModelAdmin(ModelAdmin):
    """Model admin for LeadModel"""

    date_hierarchy = "created_at"
    search_fields = ["email", "first_name", "last_name", "phone", "singup_ip_address"]
    list_filter = [
        "lead_source",
        "is_subscribed",
        "was_activated",
        "was_customer",
        "detected_bot_click",
        "last_email_date",
        "last_email_opened",
        "last_email_clicked",
        "last_purchase_date",
        "last_activity_date",
    ]
    list_display = [
        "__str__",
        "is_subscribed",
        "was_activated",
        "lead_source",
        "singup_ip_address",
    ]
