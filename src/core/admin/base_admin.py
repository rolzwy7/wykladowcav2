from django.contrib import admin

from core.models import (
    Eventlog,
    LecturerOpinion,
    User,
    WebinarApplication,
    WebinarApplicationMetadata,
    WebinarApplicationSubmitter,
    WebinarParticipant,
    WebinarParticipantMetadata,
)

admin.site.register(User)
admin.site.register(Eventlog)
admin.site.register(LecturerOpinion)
admin.site.register(WebinarApplicationMetadata)
admin.site.register(WebinarParticipant)
admin.site.register(WebinarParticipantMetadata)
admin.site.register(WebinarApplication)
admin.site.register(WebinarApplicationSubmitter)
