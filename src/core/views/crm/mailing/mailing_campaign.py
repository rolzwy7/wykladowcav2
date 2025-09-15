"""Mailing campaign pages"""

# flake8: noqa=E501
# pylint: disable=broad-exception-caught

from datetime import datetime, timedelta

from django.conf import settings
from django.core.cache import cache
from django.core.mail.utils import DNS_NAME
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import now

from core.consts import POST
from core.forms import (
    MailingAddEmailsForm,
    MailingAreYouSureForm,
    MailingSendTestEmailForm,
)
from core.libs.mailing.test_email import send_campaign_test_email
from core.models import (
    ListRBL,
    MailingCampaign,
    MailingTemplate,
    MonitorRBL,
    SmtpSender,
    WebinarMetadata,
)
from core.models.enums import mailing_pool_status_display_map
from core.models.mailing import MailingPoolManager
from core.services.mailing import MailingCampaignService

BASE_URL = settings.BASE_URL


def crm_mailing_campaign_list(request):
    """CRM mailing campaigns list"""

    show_grid = request.GET.get("show_grid", "")

    show_all = request.GET.get("show_all", "")
    if show_all:
        qs = MailingCampaign.manager.all().order_by("-created_at")[:75]
    else:
        qs = MailingCampaign.manager.not_done().order_by("-created_at")

    try:
        fqdn = DNS_NAME.get_fqdn()
    except Exception as e:
        fqdn = f"FQDN Błąd {e}"

    mailing_campaigns = [
        (
            campaign,
            WebinarMetadata.objects.filter(webinar=campaign.webinar).first(),
        )
        for campaign in qs
    ]

    favourite_mailing_campaigns = [
        (
            campaign,
            WebinarMetadata.objects.filter(webinar=campaign.webinar).first(),
        )
        for campaign in MailingCampaign.manager.favourite()
    ]

    # Get campaings where error occured
    mailing_errors = MailingCampaign.manager.filter(
        Q(any_error_occured=True)
        | Q(smtp_server_disconnected=True)
        | Q(connection_refused=True)
    )

    # RBL lists
    cache_key = "monitored_senders_list"
    monitored_senders_list = cache.get(cache_key)

    if monitored_senders_list is None:
        monitored_senders = SmtpSender.objects.filter(
            Q(show_on_crm_panel=True) & Q(monitor_rbl=True)
        )
        monitored_senders_list = []
        for monitored_sender in monitored_senders:
            monitored_senders_list.append(
                (
                    monitored_sender.username,
                    monitored_sender.domain,
                    [
                        MonitorRBL.manager.get_latest(monitored_sender.domain, rbl_list)
                        for rbl_list in ListRBL.manager.all()
                    ],
                    monitored_sender.ip_address,
                    [
                        MonitorRBL.manager.get_latest(
                            monitored_sender.ip_address, rbl_list
                        )
                        for rbl_list in ListRBL.manager.all()
                    ],
                )
            )
        cache.set(cache_key, monitored_senders_list, 60 * 5)  # 5 minutes cache

    return TemplateResponse(
        request,
        "core/pages/crm/mailing/MailingCampaignListPage.html",
        {
            "monitored_senders_list": monitored_senders_list,
            "favourite_mailings": favourite_mailing_campaigns,
            "mailing_errors": mailing_errors,
            "tuple_list": mailing_campaigns,
            "fqdn": fqdn,
            "show_all": show_all,
            "show_grid": show_grid,
            "now": now(),
            "smpt_senders": SmtpSender.objects.filter(exclude_from_processing=False),
            "today_datestr": datetime.now().strftime("%Y-%m-%d"),
            "yesterday_datestr": (datetime.now() - timedelta(1)).strftime("%Y-%m-%d"),
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

            send_campaign_test_email(email, mailing_campaign)

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
            service.reset_campaign()
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


def crm_mailing_campaign_duplicate(request, pk: int):
    """CRM mailing reset emails"""
    template_name = "core/pages/crm/mailing/MailingCampaignDuplicate.html"
    mailing_campaign = get_object_or_404(MailingCampaign, pk=pk)

    if request.method == POST:
        form = MailingAreYouSureForm(request.POST)
        if form.is_valid():

            mailing_campaign.id = None  # type: ignore
            mailing_campaign.title = f"COPY_{mailing_campaign.title}"
            mailing_campaign.save()
            service = MailingCampaignService(mailing_campaign)
            service.reset_campaign()

            # Duplicate template
            template = MailingTemplate.objects.get(id=mailing_campaign.template.id)
            template.id = None  # type: ignore
            template.name = f"fromcopy_{mailing_campaign.id}_{template.name}"  # type: ignore
            template.save()

            mailing_campaign.template = template
            mailing_campaign.save()

            return redirect(
                reverse(
                    "core:crm_mailing_campaign_detail",
                    kwargs={"pk": mailing_campaign.id},  # type: ignore
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


def crm_mailing_campaign_download_emails(request, pk: int):
    """crm_mailing_campaign_download_emails"""

    campaign = get_object_or_404(MailingCampaign, pk=pk)
    campaign_id: int = campaign.id  # type: ignore

    status = request.GET.get("status", "")

    mongo_filter = {"campaign_id": campaign_id}
    if status:
        mongo_filter["status"] = status

    manager = MailingPoolManager()
    emails = [document["email"] for document in manager.collection.find(mongo_filter)]
    manager.close()

    return HttpResponse(
        "\n".join(set(emails)),
        content_type="text/plain; charset=utf8",
        headers={
            "Content-Disposition": f'inline; filename="CAMPAIG_ID_{campaign_id}_{status}.txt"'
        },
    )
