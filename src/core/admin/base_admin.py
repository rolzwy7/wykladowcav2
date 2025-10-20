"""
Base admin
"""

# flake8: noqa=E501

from django.contrib import admin
from django.contrib.admin import ModelAdmin, register

from core.models import (
    AdvertPopup,
    AdvertPopupClick,
    BlogView,
    CategoryTrustedUs,
    ClosedWebinarContactMessage,
    ConferenceChat,
    ConferenceChatMessage,
    ContactMessage,
    CrmCompany,
    CrmContact,
    CrmNote,
    CustomHtmlSite,
    DiscountApplicationApplied,
    Eventlog,
    FakturowniaCategory,
    ListRBL,
    LoyaltyProgram,
    LoyaltyProgramIncome,
    LoyaltyProgramPayout,
    MailingCampaign,
    MailingReplyMessage,
    MailingScheduled,
    MailingTemplate,
    MonitorRBL,
    SaleRecording,
    SaleRecordingApplication,
    ServiceOffer,
    ServiceOfferLead,
    SmtpSender,
    SpyObject,
    Survey,
    SurveyAnswer,
    SurveyOpinion,
    SurveyVote,
    WebinarApplicationCancellation,
    WebinarApplicationCompany,
    WebinarApplicationInvoice,
    WebinarApplicationMetadata,
    WebinarApplicationPrivatePerson,
    WebinarApplicationSubmitter,
    WebinarApplicationTracking,
    WebinarAsset,
    WebinarMoveRegister,
    WebinarMoveRegisterItem,
    WebinarRecording,
    WebinarRecordingToken,
)

admin.site.register(ConferenceChat)

admin.site.register(BlogView)


@register(ConferenceChatMessage)
class ConferenceChatMessageModelAdmin(ModelAdmin):
    """ConferenceChatMessage ModelAdmin."""

    date_hierarchy = "created_at"
    list_display = (
        "chat",
        "chat_user",
        "status",
        "created_at",
        "perspective_score",
        "message",
    )
    list_filter = ("status",)
    search_fields = ("message",)
    raw_id_fields = ("chat", "chat_user")


@register(ListRBL)
class ListRBLModelAdmin(ModelAdmin):
    """ListRBL ModelAdmin."""

    search_fields = ("address",)
    list_filter = ("list_type", "is_important_list")
    list_display = ("address", "is_important_list", "list_type")


admin.site.register(MonitorRBL)

admin.site.register(ClosedWebinarContactMessage)

admin.site.register(AdvertPopup)
admin.site.register(AdvertPopupClick)

admin.site.register(SpyObject)

admin.site.register(CrmNote)

admin.site.register(MailingScheduled)


@register(SaleRecording)
class SaleRecordingModelAdmin(ModelAdmin):
    """SaleRecording ModelAdmin."""

    list_display = ("__str__", "is_visible", "recording")
    # search_fields = ("webinar__title", "student__email")


@register(SaleRecordingApplication)
class SaleRecordingApplicationModelAdmin(ModelAdmin):
    """SaleRecordingApplication ModelAdmin."""

    date_hierarchy = "created_at"
    list_display = (
        "id",
        "status",
        "application_type",
        "sale_recording",
        "created_at",
        "price_netto",
    )
    list_filter = ("status", "application_type", "sale_recording")
    search_fields = (
        "id",
        "uuid",
        "buyer__name",
        "buyer__nip",
        "private_person__email",
        "private_person__first_name",
        "private_person__last_name",
    )


admin.site.register(SurveyAnswer)
admin.site.register(Survey)
admin.site.register(SurveyVote)
admin.site.register(SurveyOpinion)

admin.site.register(WebinarApplicationTracking)
admin.site.register(CustomHtmlSite)

admin.site.register(ServiceOffer)
admin.site.register(ServiceOfferLead)

admin.site.register(FakturowniaCategory)


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


admin.site.register(ContactMessage)

admin.site.register(CategoryTrustedUs)

admin.site.register(MailingTemplate)


@register(SmtpSender)
class SmtpSenderModelAdmin(ModelAdmin):
    """SmtpSender ModelAdmin."""

    list_display = (
        "username",
        "mailing_server",
        "bucket_id",
        "ip_address",
        "ssl",
        "exclude_from_processing",
        "monitor_rbl",
        "talos_ip_reputation",
    )
    list_filter = (
        "ssl",
        "show_on_crm_panel",
        "exclude_from_processing",
        "monitor_rbl",
        "talos_ip_reputation",
    )
    search_fields = ("sender_alias", "username", "domain", "ip_address")
    readonly_fields = ("talos_ip_reputation_checked_at",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "sender_alias",
                    "username",
                    "password",
                    "domain",
                    "reply_to",
                    "return_path",
                )
            },
        ),
        (
            "Incoming Server",
            {"fields": ("incoming_server_hostname", "incoming_server_port")},
        ),
        (
            "Outgoing Server",
            {"fields": ("outgoing_server_hostname", "outgoing_server_port")},
        ),
        (
            "Configuration",
            {
                "fields": (
                    "ssl",
                    "exclude_from_processing",
                    "mailing_server",
                    "bucket_id",
                    "show_on_crm_panel",
                    "ip_address",
                    "base_url_override",
                )
            },
        ),
        (
            "Monitoring",
            {
                "fields": (
                    "monitor_rbl",
                    "talos_ip_reputation",
                    "talos_ip_reputation_checked_at",
                )
            },
        ),
        (
            "Override",
            {
                "fields": (
                    "resignation_list",
                    "allowed_to_send_after",
                    "allowed_to_send_before",
                    "sending_batch_size",
                    "sleep_between_batches",
                    "sleep_every_send",
                )
            },
        ),
    )


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
admin.site.register(WebinarApplicationMetadata)
admin.site.register(WebinarApplicationSubmitter)
admin.site.register(WebinarRecording)
admin.site.register(WebinarRecordingToken)
