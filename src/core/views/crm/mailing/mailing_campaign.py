"""Mailing campaign pages"""

# flake8: noqa=E501

from django.conf import settings
from django.core.mail.utils import DNS_NAME
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import (
    MailingAddEmailsForm,
    MailingAreYouSureForm,
    MailingSendTestEmailForm,
)
from core.models import MailingCampaign, MailingTemplate, WebinarMetadata
from core.models.enums import mailing_pool_status_display_map
from core.models.mailing import MailingPoolManager
from core.services import SenderSmtpService
from core.services.mailing import (
    MailingCampaignService,
    MailingResignationService,
    MailingTrackingService,
)

BASE_URL = settings.BASE_URL


def crm_mailing_campaign_list(request):
    """CRM mailing campaigns list"""
    template_name = "core/pages/crm/mailing/MailingCampaignListPage.html"

    show_all = request.GET.get("show_all", "")
    if show_all:
        qs = MailingCampaign.manager.all().order_by("-created_at")[:75]
    else:
        qs = MailingCampaign.manager.not_done().order_by("-created_at")

    try:
        fqdn = DNS_NAME.get_fqdn()
    except Exception as e:
        fqdn = "FQDN Błąd"

    mailing_campaigns = [
        (
            campaign,
            WebinarMetadata.objects.filter(webinar=campaign.webinar).first(),
        )
        for campaign in qs
    ]

    return TemplateResponse(
        request,
        template_name,
        {
            "tuple_list": mailing_campaigns,
            "fqdn": fqdn,
            "show_all": show_all,
        },
    )


def crm_mailing_campaign_detail(request, pk: int):
    """CRM mailing add emails"""
    template_name = "core/pages/crm/mailing/MailingCampaignDetailPage.html"
    mailing_campaign = get_object_or_404(MailingCampaign, pk=pk)
    mailing_campaign_id: int = mailing_campaign.id  # type: ignore
    service = MailingCampaignService(mailing_campaign)

    return TemplateResponse(
        request,
        template_name,
        {
            "mailing_campaign": mailing_campaign,
            "spam_phrases": service.get_spam_phrases,
            "emails_count": service.get_email_count_for_campaign(mailing_campaign_id),
            "statuses": service.group_by_count_statuses(mailing_campaign_id),
        },
    )


def crm_mailing_campaign_add_emails(request, pk: int):
    """CRM mailing add emails"""
    template_name = "core/pages/crm/mailing/MailingCampaignAddEmailsPage.html"
    mailing_campaign = get_object_or_404(MailingCampaign, pk=pk)
    mailing_campaign_id: int = mailing_campaign.id  # type: ignore
    service = MailingCampaignService(mailing_campaign)

    if request.method == POST:
        form = MailingAddEmailsForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
            service.load_emails_from_file_into_campaign(file)
            return redirect(
                reverse(
                    "core:crm_mailing_campaign_detail",
                    kwargs={"pk": mailing_campaign.pk},
                )
            )
    else:
        form = MailingAddEmailsForm()

    return TemplateResponse(
        request,
        template_name,
        {
            "form": form,
            "mailing_campaign": mailing_campaign,
            "emails_count": service.get_email_count_for_campaign(mailing_campaign_id),
        },
    )


def crm_mailing_campaign_send_test_email(request, pk: int):
    """CRM mailing add emails"""
    template_name = "core/pages/crm/mailing/MailingCampaignSendTestEmailPage.html"
    mailing_campaign = get_object_or_404(MailingCampaign, pk=pk)

    if request.method == POST:
        form = MailingSendTestEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            service = SenderSmtpService(mailing_campaign.smtp_sender)

            template: MailingTemplate = mailing_campaign.template

            resignation_code = (
                MailingResignationService.get_or_create_inactive_resignation(
                    email, mailing_campaign.resignation_list
                )
            )
            resignation_url = BASE_URL + reverse(
                "core:mailing_resignation_page_with_list",
                kwargs={
                    "resignation_code": resignation_code,
                    "resignation_list": mailing_campaign.resignation_list,
                },
            )
            tracking_code = MailingTrackingService.get_or_create_tracking(email)

            with service.get_smtp_connection() as connection:
                service.send_email(
                    connection=connection,
                    email=email,
                    alias=mailing_campaign.alias,
                    subject=mailing_campaign.get_random_subject(),
                    html=template.html,
                    text=template.text,
                    resignation_url=resignation_url,
                    tracking_code=tracking_code,
                )

            return redirect(
                reverse(
                    "core:crm_mailing_campaign_detail",
                    kwargs={"pk": mailing_campaign.pk},
                )
            )
    else:
        form = MailingSendTestEmailForm()

    return TemplateResponse(
        request,
        template_name,
        {"form": form, "mailing_campaign": mailing_campaign},
    )


def crm_mailing_campaign_delete_emails(request, pk: int):
    """CRM mailing add emails"""
    template_name = "core/pages/crm/mailing/MailingCampaignDeleteEmailsPage.html"
    mailing_campaign = get_object_or_404(MailingCampaign, pk=pk)
    service = MailingCampaignService(mailing_campaign)

    if request.method == POST:
        form = MailingAreYouSureForm(request.POST)
        if form.is_valid():
            service.delete_all_emails()
            return redirect(
                reverse(
                    "core:crm_mailing_campaign_detail",
                    kwargs={"pk": mailing_campaign.pk},
                )
            )
    else:
        form = MailingAreYouSureForm()

    mailing_campaign = get_object_or_404(MailingCampaign, pk=pk)
    return TemplateResponse(
        request,
        template_name,
        {"form": form, "mailing_campaign": mailing_campaign},
    )


def crm_mailing_campaign_reset_emails(request, pk: int):
    """CRM mailing reset emails"""
    template_name = "core/pages/crm/mailing/MailingCampaignResetEmails.html"
    mailing_campaign = get_object_or_404(MailingCampaign, pk=pk)
    service = MailingCampaignService(mailing_campaign)

    if request.method == POST:
        form = MailingAreYouSureForm(request.POST)
        if form.is_valid():
            service.reset_all_emails()
            return redirect(
                reverse(
                    "core:crm_mailing_campaign_detail",
                    kwargs={"pk": mailing_campaign.pk},
                )
            )
    else:
        form = MailingAreYouSureForm()

    mailing_campaign = get_object_or_404(MailingCampaign, pk=pk)
    return TemplateResponse(
        request,
        template_name,
        {"form": form, "mailing_campaign": mailing_campaign},
    )


def crm_mailing_campaign_preview_html(request, pk: int):
    """Mailing campaign preview HTML version"""
    mailing_campaign = get_object_or_404(MailingCampaign, pk=pk)
    template: MailingTemplate = mailing_campaign.template
    return HttpResponse(template.html, content_type="text/html; charset=utf8")


def crm_mailing_campaign_preview_text(request, pk: int):
    """Mailing campaign preview TEXT version"""
    mailing_campaign = get_object_or_404(MailingCampaign, pk=pk)
    template: MailingTemplate = mailing_campaign.template
    return HttpResponse(template.text, content_type="text/plain; charset=utf8")


# TODO: crm_mailing_campaign_email_search_page
def crm_mailing_campaign_email_search_page(request, pk: int):
    """Search for emails in mailing campaign"""
    template_path = "core/pages/crm/mailing/MailingCampaignEmailSearchPage.html"
    campaign = get_object_or_404(MailingCampaign, pk=pk)
    campaign_id: int = campaign.id  # type: ignore

    email_regex = request.GET.get("email_regex", "")
    status = request.GET.get("status", "")

    mongo_filter = {"campaign_id": campaign_id}

    if status:
        mongo_filter["status"] = status
    if email_regex:
        mongo_filter["email"] = {"$regex": email_regex}

    manager = MailingPoolManager()
    pool = [
        (document["email"], document["status"])
        for document in manager.collection.find(mongo_filter).limit(50)
    ]
    manager.close()

    return TemplateResponse(
        request,
        template_path,
        {
            "campaign": campaign,
            "pool": pool,
            "email_regex": email_regex,
            "status": status,
            "status_select_options": [
                *[("", "Wszystkie")],
                *[
                    (key, value)
                    for key, value in mailing_pool_status_display_map.items()
                ],
            ],
        },
    )
