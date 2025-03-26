"""Mailing clicks stats"""

# flake8: noqa=E501

import re

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.libs.mongo.db import MongoDBClient
from core.models import Webinar
from core.models.mailing import MailingCampaign


def crm_mailing_clicks_stats(request, pk):
    """crm_mailing_clicks_stats"""
    template_name = "core/pages/crm/mailing/MailingClicksStats.html"

    campaign = get_object_or_404(MailingCampaign, pk=pk)
    campaign_id: int = campaign.id  # type: ignore

    _, database = MongoDBClient.get_connection()
    click_docs = database["wykladowcav2_mailing_clicks"].find({"campaign_id": pk})

    per_url: dict[str, dict] = {}
    per_webinar: dict[int, dict] = {}

    for doc in click_docs:
        request_url = doc.get("request_url") or "Brak Danych"

        # Group by count clicks
        if request_url in per_url:
            per_url[request_url]["click_count"] += 1
        else:
            per_url[request_url] = {"click_count": 1}

        # Get webinar ID
        pattern = r"https://wykladowca\.pl/szkl/(\d+)/"
        re_webinar_id = re.search(pattern, request_url)
        webinar_id = int(re_webinar_id.group(1)) if re_webinar_id else None
        per_url[request_url]["webinar_id"] = webinar_id

        # Get webinar
        if webinar_id:
            webinar = Webinar.manager.filter(id=webinar_id).first()
            if webinar_id in per_webinar:
                per_webinar[webinar_id]["click_count"] += 1
            else:
                per_webinar[webinar_id] = {"click_count": 1}
            per_webinar[webinar_id]["webinar"] = webinar
        else:
            webinar = None
        per_url[request_url]["webinar"] = webinar

    return TemplateResponse(
        request,
        template_name,
        {
            "campaign": campaign,
            "per_url": dict(
                sorted(per_url.items(), key=lambda x: x[1]["click_count"], reverse=True)
            ),
            "per_webinar": dict(
                sorted(
                    per_webinar.items(), key=lambda x: x[1]["click_count"], reverse=True
                )
            ),
        },
    )
