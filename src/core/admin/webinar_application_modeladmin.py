from django.contrib.admin import ModelAdmin, register

from core.models import WebinarApplication


@register(WebinarApplication)
class WebinarApplicationModelAdmin(ModelAdmin):
    readonly_fields = ["uuid"]
