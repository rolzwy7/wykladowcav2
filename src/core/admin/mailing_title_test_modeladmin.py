"""
MailingTitleTest Model Admin
"""

from django.contrib.admin import ModelAdmin, register

from core.models import MailingTitleTest


@register(MailingTitleTest)
class MailingTitleTestModelAdmin(ModelAdmin):
    """MailingTitleTestModelAdmin"""

    search_fields = [
        "title",
        "sha256_hash",
    ]
    list_display = [
        "id",
        "campaign_id",
        "title",
        "sha256_hash",
        "counter",
    ]
