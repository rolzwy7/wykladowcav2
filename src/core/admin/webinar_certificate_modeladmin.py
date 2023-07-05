from django.contrib.admin import ModelAdmin, register

from core.models import WebinarCertificate


@register(WebinarCertificate)
class WebinarCertificateModelAdmin(ModelAdmin):
    readonly_fields = ["uuid"]
    search_fields = ["first_name", "last_name", "title"]

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
