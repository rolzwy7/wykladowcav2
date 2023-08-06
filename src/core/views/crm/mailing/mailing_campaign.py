from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import MailingAddEmailsForm, MailingDeleteEmailsAreYouSureForm
from core.models import MailingCampaign
from core.services import MailingCampaignService


def crm_mailing_campaign_list(request):
    """CRM mailing campaigns list"""
    template_name = "core/pages/crm/mailing/MailingCampaignListPage.html"
    return TemplateResponse(
        request,
        template_name,
        {"mailing_campaigns": MailingCampaign.objects.all()},
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
            "emails_count": service.get_email_count_for_campaign(
                mailing_campaign_id
            ),
            "statuses": service.group_by_count_statuses(mailing_campaign_id),
        },
    )


def crm_mailing_campaign_add_emails(request, pk: int):
    """CRM mailing add emails"""
    template_name = "core/pages/crm/mailing/MailingCampaignAddEmailsPage.html"
    mailing_campaign = get_object_or_404(MailingCampaign, pk=pk)
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
        {"form": form, "mailing_campaign": mailing_campaign},
    )


def crm_mailing_campaign_delete_emails(request, pk: int):
    """CRM mailing add emails"""
    template_name = (
        "core/pages/crm/mailing/MailingCampaignDeleteEmailsPage.html"
    )
    mailing_campaign = get_object_or_404(MailingCampaign, pk=pk)
    service = MailingCampaignService(mailing_campaign)

    if request.method == POST:
        form = MailingDeleteEmailsAreYouSureForm(request.POST)
        if form.is_valid():
            service.delete_all_emails()
            return redirect(
                reverse(
                    "core:crm_mailing_campaign_detail",
                    kwargs={"pk": mailing_campaign.pk},
                )
            )
    else:
        form = MailingDeleteEmailsAreYouSureForm()

    mailing_campaign = get_object_or_404(MailingCampaign, pk=pk)
    return TemplateResponse(
        request,
        template_name,
        {"form": form, "mailing_campaign": mailing_campaign},
    )
