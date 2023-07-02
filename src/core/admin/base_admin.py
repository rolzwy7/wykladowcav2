from django.contrib import admin

from core.models import (
    LecturerOpinion,
    User,
    WebinarApplication,
    WebinarApplicationSubmitter,
    WebinarEventlog,
    WebinarParticipant,
    WebinarParticipantMetadata,
)

admin.site.register(User)
admin.site.register(WebinarEventlog)
admin.site.register(LecturerOpinion)
admin.site.register(WebinarParticipant)
admin.site.register(WebinarParticipantMetadata)
admin.site.register(WebinarApplication)
admin.site.register(WebinarApplicationSubmitter)
