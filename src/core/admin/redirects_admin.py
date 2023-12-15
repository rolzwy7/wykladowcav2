from django.contrib.admin import ModelAdmin, register

from core.models import RedirectManual


@register(RedirectManual)
class RedirectManualModelAdmin(ModelAdmin):
    """Model admin for `RedirectManual` model"""

    search_fields = ["slug", "url"]
    list_display = ["slug", "url", "status_code", "counter"]
    list_filter = ["status_code"]
