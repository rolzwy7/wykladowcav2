"""Webinar Application Model Admin"""

# flake8: noqa=E501

from django.contrib.admin import ModelAdmin, register
from django.utils.html import format_html

from core.models import WebinarApplication


@register(WebinarApplication)
class WebinarApplicationModelAdmin(ModelAdmin):
    """WebinarApplicationModelAdmin"""

    list_display = ["uuid", "status", "application_type", "buyer_htmlfield"]
    list_filter = ["status", "application_type", "got_to_summary"]
    date_hierarchy = "created_at"

    search_fields = [
        "uuid",
        "recipient__nip",
        "recipient__name",
        "recipient__address",
        "buyer__nip",
        "buyer__name",
        "buyer__address",
        "private_person__first_name",
        "private_person__last_name",
        "private_person__address",
    ]

    readonly_fields = ["uuid"]

    def buyer_htmlfield(self, application):
        """Buyer HTML field"""
        html = ""
        if application.recipient:
            html += f"<p>Nabywca: ({application.recipient.nip}) {application.recipient.name}</p>"
        if application.buyer:
            html += (
                f"<p>Odbiorca: ({application.buyer.nip}) {application.buyer.name}</p>"
            )
        if application.private_person:
            pp = application.private_person
            html += f"<p>Osoba prywatna: {pp.first_name} {pp.last_name} {pp.email} {pp.phone}</p>"
        return format_html(html)  # noqa
