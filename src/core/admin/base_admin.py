from django.contrib import admin

from core.models import (
    CrmCompany,
    CrmContact,
    DiscountApplicationApplied,
    DiscountCode,
    Eventlog,
    LecturerOpinion,
    User,
    WebinarApplication,
    WebinarApplicationMetadata,
    WebinarApplicationSubmitter,
    WebinarAsset,
    WebinarParticipant,
    WebinarParticipantMetadata,
    WebinarRecording,
    WebinarRecordingToken,
)

admin.site.register(User)
admin.site.register(DiscountCode)
admin.site.register(DiscountApplicationApplied)
admin.site.register(CrmCompany)
admin.site.register(CrmContact)
admin.site.register(WebinarAsset)
admin.site.register(Eventlog)
admin.site.register(LecturerOpinion)
admin.site.register(WebinarApplicationMetadata)
admin.site.register(WebinarParticipant)
admin.site.register(WebinarParticipantMetadata)
admin.site.register(WebinarApplication)
admin.site.register(WebinarApplicationSubmitter)
admin.site.register(WebinarRecording)
admin.site.register(WebinarRecordingToken)
