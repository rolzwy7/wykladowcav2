from django.contrib.admin import ModelAdmin, register
from django.utils.html import format_html

from core.models import WebinarCertificate


@register(WebinarCertificate)
class WebinarCertificateModelAdmin(ModelAdmin):
    """Model admin for `WebinarCertificate` model"""

    readonly_fields = ["uuid"]
    search_fields = ["first_name", "last_name", "title", "uuid"]
    list_display = [
        "uuid",
        "first_name",
        "last_name",
        "title",
        "issue_date",
        "hours",
        "actions_view",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "uuid",
                    ("first_name", "last_name"),
                    "title",
                    "issue_date",
                    "hours",
                    "participant",
                ],
            },
        ),
    )

    def get_sortable_by(self, request):
        return {*self.get_list_display(request)} - {"uuid"}

    def actions_view(self, obj: WebinarCertificate):
        """Actions for list element"""
        return format_html(
            '<a href="{}" target="_blank">Podgląd</a>', obj.get_absolute_url()
        )
