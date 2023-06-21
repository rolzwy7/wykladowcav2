from django.contrib.admin import ModelAdmin, register
from django.utils.html import format_html

from core.models import Lecturer


@register(Lecturer)
class LecturerModelAdmin(ModelAdmin):
    def avatar_image_preview(self, lecturer):
        return format_html(
            f'<img src="{lecturer.avatar.url}" style="max-width: 200px; height: auto;" />'  # noqa
        )

    prepopulated_fields = {"slug": ("fullname",)}
    filter_horizontal = ("categories",)
    readonly_fields = ["avatar_image_preview"]
