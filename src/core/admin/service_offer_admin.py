from django.contrib import admin
from django.contrib.admin import ModelAdmin, register

from core.models import ServiceOfferApplication


@register(ServiceOfferApplication)
class ServiceOfferApplicationModelAdmin(ModelAdmin):
    """ServiceOfferApplicationModelAdmin"""

    # filter_horizontal = ("categories",)
    # list_display = ["title", "date", "status", "lecturer", "price_netto"]
    # search_fields = [
    #     "title_original",
    #     "title",
    #     "slug",
    # ]
    # date_hierarchy = "created_at"
    # list_filter = [
    #     "status",
    #     "is_confirmed",
    #     "is_fake",
    #     "show_lecturer",
    #     "is_hidden",
    #     "recording_allowed",
    # ]

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "status",
                    "uncertain",
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
