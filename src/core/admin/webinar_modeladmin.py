# flake8: noqa:DJ07

from django import forms
from django.contrib.admin import ModelAdmin, StackedInline, register
from django.forms import ModelForm
from tinymce.widgets import TinyMCE

from core.models import Webinar, WebinarCategory, WebinarMetadata


class WebinarModelAdminInline(StackedInline):
    """Webinar Model Admin Inline"""

    model = WebinarMetadata
    can_delete = False
    classes = ["collapse"]


class WebinarModelAdminForm(ModelForm):
    """Webinar Model Admin Form"""

    class Meta:
        model = Webinar
        fields = "__all__"
        widgets = {"program": TinyMCE(attrs={"cols": 80, "rows": 30})}

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields["categories"].queryset = WebinarCategory.manager.all().order_by(
            "parent__name"
        )


@register(Webinar)
class WebinarModelAdmin(ModelAdmin):
    """Webinar Model Admin"""

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        # Add lecturer's categories to webinar after save
        webinar = form.instance
        for category in webinar.lecturer.categories.all():
            webinar.categories.add(category)

    form = WebinarModelAdminForm
    inlines = [
        WebinarModelAdminInline,
    ]
    # prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories",)
    list_display = ["title", "date", "status", "lecturer", "price_netto"]
    search_fields = [
        "title_original",
        "title",
        "slug",
    ]
    date_hierarchy = "date"
    list_filter = [
        "status",
        "is_confirmed",
        "is_fake",
        "show_lecturer",
        "is_hidden",
        "recording_allowed",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "show_lecturer",
                    "is_hidden",
                    "is_confirmed",
                    "recording_allowed",
                    "is_fake",
                    "remaining_places",
                    "facebook_post_image",
                    ("status", "slug"),
                    ("date", "duration"),
                    ("lecturer", "grouping_token"),
                    "title_original",
                    "title",
                    "description",
                ],
            },
        ),
        # (
        #     "Data",
        #     {
        #         "fields": ["date", "duration"],
        #     },
        # ),
        (
            "Cena",
            {
                "fields": ["price_netto", "discount_until", "discount_netto"],
            },
        ),
        (
            "Program szkolenia",
            {
                "fields": ["program"],
            },
        ),
        (
            "Kategorie",
            {
                "fields": [
                    "categories",
                ],
            },
        ),
        (
            "Program (inne formy)",
            {
                "classes": ["collapse"],
                "fields": [
                    "program_markdown",
                    "program_pretty",
                    "program_short",
                ],
            },
        ),
        (
            "Zewnętrzny dostawca",
            {
                "classes": ["collapse"],
                "fields": [
                    "external_name",
                    "external_url",
                    "external_description",
                ],
            },
        ),
        (
            "Konferencja",
            {
                "classes": ["collapse"],
                "fields": [
                    "is_connected_to_conference",
                ],
            },
        ),
    )
