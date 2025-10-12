# flake8: noqa:DJ07

from django.contrib.admin import ModelAdmin, register
from django.forms import ModelForm
from tinymce.widgets import TinyMCE

from core.models import WebinarAggregate


class WebinarAggregateModelAdminForm(ModelForm):
    """Webinar Model Admin Form"""

    class Meta:
        model = WebinarAggregate
        fields = "__all__"
        widgets = {
            "program": TinyMCE(attrs={"cols": 80, "rows": 30}),
            "program_assets": TinyMCE(attrs={"cols": 80, "rows": 30}),
        }


@register(WebinarAggregate)
class WebinarAggregateModelAdmin(ModelAdmin):
    """WebinarAggregateModelAdmin"""

    form = WebinarAggregateModelAdminForm

    list_display = ["__str__", "slug", "slug_conflict", "parent"]
    search_fields = ["grouping_token", "slug", "title"]
    filter_horizontal = ("categories",)
    list_filter = ["categories", "lecturer"]

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "hidden",
                    "pod_szkolenie_zamkniete",
                    "grouping_token",
                    "slug",
                    "closest_webinar_dt",
                    "has_active_webinars",
                    "lecturer",
                    "title",
                    "short_description",
                    "program_assets",
                    "program",
                    "program_short",
                    "categories",
                    "webinars",
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
                    "program_assets_conflict",
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
        (
            "Advert",
            {
                "fields": [
                    "title_blogpost_advert",
                ],
            },
        ),
    )
