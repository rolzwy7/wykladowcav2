from django.contrib.admin import ModelAdmin, StackedInline, register
from django.db.models import TextField
from django.forms.widgets import Textarea

from core.models import Webinar, WebinarMetadata


class WebinarModelAdminInline(StackedInline):
    model = WebinarMetadata
    can_delete = False
    classes = ["collapse"]
    readonly_fields = ["clickmeeting_id"]


@register(Webinar)
class WebinarModelAdmin(ModelAdmin):
    inlines = [
        WebinarModelAdminInline,
    ]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories",)
    list_display = ["title", "date", "status", "lecturer", "price_netto"]
    formfield_overrides = {
        TextField: {"widget": Textarea(attrs={"rows": 5, "cols": 80})},
    }

    fieldsets = (
        (
            None,
            {
                "fields": [
                    ("status", "slug"),
                    "lecturer",
                    "title_original",
                    "title",
                    "description",
                    "categories",
                ],
            },
        ),
        (
            "Data",
            {
                "fields": ["date", "duration"],
            },
        ),
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
    )
