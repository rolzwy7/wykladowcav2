"""Mailing Refetch Template"""

# flake8: noqa=E501

import requests
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import MailingAreYouSureForm
from core.models import MailingCampaign, MailingTemplate


def crm_mailing_refetch_template(request, pk: int):
    """crm_mailing_refetch_template"""
    template_name = "core/pages/crm/mailing/MailingRefetchTemplatePage.html"
    mailing_campaign = get_object_or_404(MailingCampaign, pk=pk)

    if not mailing_campaign.template_url:
        return HttpResponse("no template_url")

    if request.method == POST:
        form = MailingAreYouSureForm(request.POST)
        if form.is_valid():

            try:
                response = requests.get(mailing_campaign.template_url, timeout=7)
                response.raise_for_status()
            except requests.HTTPError as e:
                return HttpResponse(f"HTTPError: {e}")
            except Exception as e:
                return HttpResponse(f"Exception: {e}")
            else:
                template = MailingTemplate.objects.get(id=mailing_campaign.template.id)
                template.text = ""
                template.html = str(response.content, "utf8")
                template.save()

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
