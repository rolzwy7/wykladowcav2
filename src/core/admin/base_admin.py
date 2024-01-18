"""
Base admin
"""
from django.contrib import admin
from django.contrib.admin import ModelAdmin, register

from core.models import (
    CategoryTrustedUs,
    ContactMessage,
    CrmCompany,
    CrmContact,
    CustomHtmlSite,
    DiscountApplicationApplied,
    Eventlog,
    LecturerOpinion,
    LoyaltyProgram,
    LoyaltyProgramIncome,
    LoyaltyProgramPayout,
    MailingCampaign,
    MailingReplyMessage,
    MailingTemplate,
    SmtpSender,
    User,
    WebinarApplication,
    WebinarApplicationCancellation,
    WebinarApplicationCompany,
    WebinarApplicationInvoice,
    WebinarApplicationMetadata,
    WebinarApplicationPrivatePerson,
    WebinarApplicationSubmitter,
    WebinarAsset,
    WebinarMoveRegister,
    WebinarMoveRegisterItem,
    WebinarParticipant,
    WebinarParticipantMetadata,
    WebinarRecording,
    WebinarRecordingToken,
)

admin.site.register(CustomHtmlSite)


@register(MailingReplyMessage)
class MailingReplyMessageModelAdmin(ModelAdmin):
    """MailingReplyMessageModelAdmin"""

    date_hierarchy = "created_at"

    list_display = [
        "from_email",
        "checked",
        "subject",
        "is_aggressor",
        "is_vacation",
        "is_email_change",
    ]

    search_fields = ["from_email", "subject", "message_content"]

    list_filter = [
        "checked",
        "is_aggressor",
        "is_vacation",
        "is_email_change",
    ]


admin.site.register(User)

admin.site.register(ContactMessage)

admin.site.register(CategoryTrustedUs)

admin.site.register(MailingTemplate)
admin.site.register(SmtpSender)
admin.site.register(MailingCampaign)

admin.site.register(LoyaltyProgram)
admin.site.register(LoyaltyProgramIncome)
admin.site.register(LoyaltyProgramPayout)

admin.site.register(WebinarMoveRegister)
admin.site.register(WebinarMoveRegisterItem)
admin.site.register(WebinarApplicationCancellation)
admin.site.register(WebinarApplicationCompany)
admin.site.register(WebinarApplicationPrivatePerson)
admin.site.register(WebinarApplicationInvoice)
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
