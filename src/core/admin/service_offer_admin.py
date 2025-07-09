"""service_offer_admin"""

from django.contrib.admin import ModelAdmin, register

from core.models import ServiceOfferApplication


@register(ServiceOfferApplication)
class ServiceOfferApplicationModelAdmin(ModelAdmin):
    """ServiceOfferApplicationModelAdmin"""

    list_display = ["id", "created_at", "name", "uncertain"]
    search_fields = [
        "name",
        "nip",
        "postal_code",
        "city",
    ]
    date_hierarchy = "created_at"
    list_filter = [
        "uncertain",
        "accepted_conditions",
        "resigned",
        "no_answer",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "notes",
                    "status",
                    "uncertain",
                    "accepted_conditions",
                    "resigned",
                    "no_answer",
                    "additional_info",
                    "first_name",
                    "last_name",
                    "email_contact",
                    "phone",
                    "file",
                ],
            },
        ),
        (
            "Firma",
            {
                "classes": ["collapse"],
                "fields": [
                    "nip",
                    "name",
                    "address",
                    "postal_code",
                    "city",
                ],
            },
        ),
        (
            "Inne",
            {
                "classes": ["collapse"],
                "fields": [
                    "service_offer",
                    "accepted_rodo",
                    "accepted_terms",
                    "tracking_code",
                    "sent_at",
                    "sent_ip_address",
                    "accepted_at",
                    "accepted_ip_address",
                    "email_confirmation",
                ],
            },
        ),
    )
