"""Create mailing from webinar"""

# flake8: noqa=E501

from datetime import time

import requests
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import now, timedelta

from core.consts.requests_consts import POST
from core.models import MailingCampaign, MailingTemplate, SmtpSender, Webinar


def create_mailing_campaign_from_webinar(request, pk: int):
    """create_mailing_campaign_from_webinar"""
    template_name = "core/pages/crm/mailing/MailingCreateFromWebinar.html"
    webinar = get_object_or_404(Webinar, pk=pk)
    smtp_senders = SmtpSender.objects.all()  # pylint: disable=no-member

    if request.method == POST:
        content_url = request.POST.get("content_url", "")
        resignation_list = request.POST.get("resignation_list", "default")
        smpt_sender_id = request.POST.get("smpt_sender_id")

        smtp_sender = SmtpSender.objects.get(  # pylint: disable=no-member
            id=int(smpt_sender_id)
        )
        campaign_title = f"{now().strftime('%Y%m%d')}_{webinar.title[:30]}"

        if content_url:
            result = requests.get(content_url, timeout=10)
            if not result.ok:
                content = "<p>RESULT NOT OK</p>"
            else:
                content = str(result.content, "utf8")
        else:
            content = "<p>PLACEHOLDER</p>"

        # Create mailing template
        template = MailingTemplate(name=campaign_title, html=content)
        template.save()

        # Start sending tomorrow as 02:00
        send_after = now()
        send_after = send_after + timedelta(days=1)
        send_after = send_after.replace(hour=2, minute=0, second=0)

        # Create subjects
        if webinar.is_connected_to_conference:
            subjects = f"Bezpłatny webinar - {webinar.title}"
        else:
            subjects = webinar.title

        campaign = MailingCampaign(
            webinar=webinar,
            title=campaign_title,
            smtp_sender=smtp_sender,
            subjects=subjects,
            alias=webinar.lecturer.fullname,
            template=template,
            resignation_list=resignation_list,
            status="SENDING",
            allowed_to_send_after=time(5, 0, 0, 0),
            allowed_to_send_before=time(23, 50, 0, 0),
            send_after=send_after,
        )
        campaign.save()

        return redirect(
            reverse("core:crm_mailing_campaign_detail", kwargs={"pk": campaign.pk})
        )

    return TemplateResponse(
        request, template_name, {"webinar": webinar, "smtp_senders": smtp_senders}
    )
