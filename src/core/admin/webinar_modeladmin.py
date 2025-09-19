# flake8: noqa:DJ07

from django import forms
from django.contrib.admin import ModelAdmin, StackedInline, register
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from simple_history.admin import SimpleHistoryAdmin
from tinymce.widgets import TinyMCE

from core.models import Webinar, WebinarCategory, WebinarMetadata
from core.models.enums.webinar_enums import WebinarStatus


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
        widgets = {
            "program": TinyMCE(attrs={"cols": 80, "rows": 30}),
            "program_assets": TinyMCE(attrs={"cols": 80, "rows": 30}),
        }

    def clean_status(self):
        """clean_status"""

        new_status = self.cleaned_data.get("status")

        if self.instance.pk:  # update
            current_status = Webinar.manager.get(pk=self.instance.pk).status
            if current_status == new_status:
                return current_status
            if current_status in [WebinarStatus.DONE, WebinarStatus.CANCELED]:
                raise ValidationError(
                    "Nie zmienić statusu w terminach Zrealizowanych/Odwołanych"
                )
        else:  # new instance
            ...

        return new_status

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields["categories"].queryset = WebinarCategory.manager.all().order_by(
            "parent__name"
        )


@register(Webinar)
class WebinarModelAdmin(SimpleHistoryAdmin):
    """Webinar Model Admin"""

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        # # Add lecturer's categories to webinar after save
        # webinar = form.instance
        # for category in webinar.lecturer.categories.all():
        #     webinar.categories.add(category)

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
        "lecturer",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "show_lecturer",
                    "anonymize_lecturer",
                    "is_hidden",
                    "is_confirmed",
                    "recording_allowed",
                    "is_fake",
                    "remaining_places",
                    "fakturownia_category",
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
            "Nagranie na sprzedaż",
            {
                "fields": [
                    "sale_recording",
                ],
            },
        ),
        (
            "Content",
            {
                "fields": ["program_assets", "program"],
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
                    "program_word_text",
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
