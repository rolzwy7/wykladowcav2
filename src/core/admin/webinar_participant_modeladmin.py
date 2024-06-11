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
    # prepopulated_fields = {"slug": ("title",)}
    # filter_horizontal = ("categories",)
    # list_display = ["title", "date", "status", "lecturer", "price_netto"]
    # search_fields = [
    #     "title_original",
    #     "title",
    #     "slug",
    # ]
    # date_hierarchy = "date"
    # list_filter = [
    #     "status",
    #     "is_confirmed",
    #     "is_fake",
    #     "show_lecturer",
    #     "is_hidden",
    #     "recording_allowed",
    # ]
