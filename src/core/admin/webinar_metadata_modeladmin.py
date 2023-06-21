from django.contrib.admin import ModelAdmin, register

from core.models import WebinarMetadata


@register(WebinarMetadata)
class WebinarMetadataModelAdmin(ModelAdmin):
    readonly_fields = ["clickmeeting_id"]
