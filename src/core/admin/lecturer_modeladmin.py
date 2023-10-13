from django.contrib.admin import ModelAdmin, register
from django.utils.html import format_html

from core.models import Lecturer


@register(Lecturer)
class LecturerModelAdmin(ModelAdmin):
    def avatar_image_preview(self, lecturer):
        """Lecturer avatar preview"""
        if lecturer.avatar:
            return format_html(
                f'<img src="{lecturer.avatar.url}" '
                'style="max-width: 200px; height: auto;" />'
            )
        return format_html("<b>Brak</b>")  # noqa

    avatar_image_preview.short_description = "Avatar - podgląd"

    prepopulated_fields = {"slug": ("fullname",)}
    filter_horizontal = ("categories",)
    readonly_fields = ["avatar_image_preview"]
