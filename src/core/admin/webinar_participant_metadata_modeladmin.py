from django.contrib.admin import ModelAdmin, register

from core.models import WebinarParticipantMetadata


@register(WebinarParticipantMetadata)
class WebinarParticipantMetadataModelAdmin(ModelAdmin):
    ...
