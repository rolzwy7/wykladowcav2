from django.contrib.admin import ModelAdmin, register

from core.models import WebinarCategory


@register(WebinarCategory)
class WebinarCategoryModelAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = [
        "name",
        "visible",
        "slug",
        "parent",
        "order",
    ]
