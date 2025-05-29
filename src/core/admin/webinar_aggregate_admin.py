# flake8: noqa:DJ07

from django.contrib.admin import ModelAdmin, register

from core.models import WebinarAggregate


@register(WebinarAggregate)
class WebinarAggregateModelAdmin(ModelAdmin):
    """WebinarAggregateModelAdmin"""

    list_display = ["__str__", "slug", "slug_conflict", "parent"]
    search_fields = ["grouping_token", "slug", "title"]
    filter_horizontal = ("categories",)

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "hidden",
                    "grouping_token",
                    "slug",
                    "closest_webinar_dt",
                    "has_active_webinars",
                    "lecturer",
                    "title",
                    "short_description",
                    "program",
                    "webinars",
                    "categories",
                ],
            },
        ),
        (
            "Nagranie na sprzedaż",
            {
                "fields": [
                    "sale_recording",
                ],
            },
        ),
        (
            "Konflikty",
            {
                "fields": [
                    "slug_conflict",
                    "title_conflict",
                    "program_conflict",
                    "lecturer_conflict",
                ],
            },
        ),
        (
            "Przekierowania",
            {
                "fields": [
                    "absolute_redirect",
                    "parent",
                ],
            },
        ),
        (
            "SEO",
            {
                "fields": [
                    "seo_meta_title",
                    "seo_meta_description",
                    "seo_canonical_url",
                ],
            },
        ),
    )


#     inlines = [
#         WebinarModelAdminInline,
#     ]
#     date_hierarchy = "date"
#     list_filter = [
#         "status",
#         "is_confirmed",
#         "is_fake",
#         "show_lecturer",
#         "is_hidden",
#         "recording_allowed",
#     ]

#     fieldsets = (
#         (
#             None,
#             {
#                 "fields": [
#                     "show_lecturer",
#                     "anonymize_lecturer",
#                     "is_hidden",
#                     "is_confirmed",
#                     "recording_allowed",
#                     "is_fake",
#                     "remaining_places",
#                     "fakturownia_category",
#                     "facebook_post_image",
#                     ("status", "slug"),
#                     ("date", "duration"),
#                     ("lecturer", "grouping_token"),
#                     "title_original",
#                     "title",
#                     "description",
#                 ],
#             },
#         ),
#         # (
#         #     "Data",
#         #     {
#         #         "fields": ["date", "duration"],
#         #     },
#         # ),
#         (
#             "Cena",
#             {
#                 "fields": ["price_netto", "discount_until", "discount_netto"],
#             },
#         ),
#         (
#             "Nagranie na sprzedaż",
#             {
#                 "fields": [
#                     "sale_recording",
#                 ],
#             },
#         ),
#         (
#             "Program szkolenia",
#             {
#                 "fields": ["program_assets", "program"],
#             },
#         ),
#         (
#             "Kategorie",
#             {
#                 "fields": [
#                     "categories",
#                 ],
#             },
#         ),
#         (
#             "Program (inne formy)",
#             {
#                 "classes": ["collapse"],
#                 "fields": [
#                     "program_markdown",
#                     "program_pretty",
#                     "program_short",
#                     "program_word_text",
#                 ],
#             },
#         ),
#         (
#             "Zewnętrzny dostawca",
#             {
#                 "classes": ["collapse"],
#                 "fields": [
#                     "external_name",
#                     "external_url",
#                     "external_description",
#                 ],
#             },
#         ),
#         (
#             "Konferencja",
#             {
#                 "classes": ["collapse"],
#                 "fields": [
#                     "is_connected_to_conference",
#                 ],
#             },
#         ),
#     )
