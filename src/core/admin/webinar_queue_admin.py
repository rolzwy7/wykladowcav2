"""
Conference admin
"""

from django.contrib import admin
from django.contrib.admin import ModelAdmin, register

from core.models import WebinarQueue


@register(WebinarQueue)
class WebinarQueueModelAdmin(ModelAdmin):
    """WebinarQueue"""

    @admin.display(description="Agregat tytuł")
    def aggregate_title(self, obj):
        """aggregate_title"""
        return obj.aggregate.title

    list_display = [
        "email",
        "created_at",
        "aggregate",
        "aggregate_title",
        "sent_notification",
        "sent_notification_at",
    ]

    search_fields = ["email", "aggregate__title", "aggregate__grouping_token"]

    list_filter = ["sent_notification"]

    date_hierarchy = "created_at"
