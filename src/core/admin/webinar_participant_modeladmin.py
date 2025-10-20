"""Webinar Participant Model Admin"""

from django.contrib.admin import ModelAdmin, StackedInline, register

from core.models import WebinarParticipant, WebinarParticipantMetadata


class WebinarParticipantModelAdminInline(StackedInline):
    """Webinar Participant Model Admin Inline"""

    model = WebinarParticipantMetadata
    can_delete = False
    classes = ["collapse"]


@register(WebinarParticipant)
class WebinarParticipantModelAdmin(ModelAdmin):
    """Webinar Participant Model Admin"""

    inlines = [WebinarParticipantModelAdminInline]
    list_display = ("id", "status", "first_name", "last_name", "email", "phone")
    list_filter = ("status", "sms_reminder_consent", "sms_reminder_send")
    search_fields = ("first_name", "last_name", "email", "phone")
