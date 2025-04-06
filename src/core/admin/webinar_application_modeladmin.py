"""Webinar Application Model Admin"""

# flake8: noqa=E501

from django.contrib.admin import ModelAdmin, StackedInline, register
from django.utils.html import format_html

from core.models import WebinarApplication, WebinarApplicationMetadata


class WebinarApplicationModelAdminInline(StackedInline):
    """WebinarApplicationModelAdmin"""

    model = WebinarApplicationMetadata
    can_delete = False
    classes = ["collapse"]

    def get_extra(self, request, obj=None, **kwargs):
        return 0


@register(WebinarApplication)
class WebinarApplicationModelAdmin(ModelAdmin):
    """WebinarApplicationModelAdmin"""

    inlines = [WebinarApplicationModelAdminInline]
    list_display = ["uuid", "status", "application_type", "buyer_htmlfield"]
    list_filter = [
        "status",
        "application_type",
        "webinar__lecturer",
        "got_to_summary",
        "webinar__status",
    ]
    date_hierarchy = "created_at"

    search_fields = [
        "uuid",
        "webinar__title",
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

        if application.webinar:
            html += f"<p><b>Webinar:</b> {application.webinar.title}"

        if application.recipient:
            html += f"<p><b>Nabywca:</b> ({application.recipient.nip}) {application.recipient.name}</p>"
        if application.buyer:
            html += f"<p><b>Odbiorca:</b> ({application.buyer.nip}) {application.buyer.name}</p>"
        if application.private_person:
            pp = application.private_person
            html += f"<p><b>Osoba prywatna:</b> {pp.first_name} {pp.last_name} {pp.email} {pp.phone}</p>"
        return format_html(html)  # noqa

    buyer_htmlfield.short_description = "Szczegóły"
