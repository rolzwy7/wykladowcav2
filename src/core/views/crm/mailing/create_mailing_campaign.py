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
from core.models.enums import MailingCampaignStatus


def create_mailing_campaign(request):
    """create_mailing_campaign"""
    template_name = "core/pages/crm/mailing/MailingCreate.html"
    smtp_senders = SmtpSender.objects.all()  # pylint: disable=no-member

    form_data = {
        "target_code": "",
        "mailing_title": "nie_ustawiono",
        "subjects": "nie_ustawiono",
        "alias": "nie_ustawiono",
        "webinar_id": "not_set",
    }

    if request.GET.get("webinar_id"):
        webinar_id = int(request.GET.get("webinar_id"))
        webinar = get_object_or_404(Webinar, pk=webinar_id)
        form_data["mailing_title"] = (
            f"{now().strftime('%Y%m%d')}_[target_code]_{webinar.title[:30]}"
        )

        if webinar.lecturer.forbid_mailing_alias:
            form_data["alias"] = "Wykładowca PL"
        else:
            form_data["alias"] = webinar.lecturer.fullname

        form_data["webinar_id"] = request.GET.get("webinar_id")

        # Create subjects
        if webinar.is_connected_to_conference:
            form_data["mailing_title"] = "KONF_" + form_data["mailing_title"]
            form_data["subjects"] = f"Bezpłatny webinar - {webinar.title}"
        else:
            form_data["subjects"] = webinar.title

        # Subject prefix
        if webinar and now() > webinar.date - timedelta(days=7):
            form_data["subjects"] = f'Ostatnia szansa: {form_data["subjects"]}'
    else:
        webinar = None
        form_data["mailing_title"] = f"{now().strftime('%Y%m%d')}_ZBIORCZY_"
        form_data["alias"] = "Wykładowca PL"

    if request.method == POST:
        webinar_id = request.POST.get("webinar_id", "not_set")
        content_url = request.POST.get("content_url", "")
        resignation_list = request.POST.get("resignation_list", "default")
        smpt_sender_id = request.POST.get("smpt_sender_id")
        mailing_title = request.POST.get("mailing_title")
        subjects = request.POST.get("subjects")
        alias = request.POST.get("alias")
        target_code = request.POST.get("target_code")

        mailing_title = mailing_title.replace("[target_code]", target_code)

        if webinar_id != "not_set":
            webinar = get_object_or_404(Webinar, pk=int(webinar_id))
        else:
            webinar = None

        smtp_sender = SmtpSender.objects.get(  # pylint: disable=no-member
            id=int(smpt_sender_id)
        )

        if content_url:
            result = requests.get(content_url, timeout=10)
            if result.ok:
                content = str(result.content, "utf8")
            else:
                content = "<p>RESULT NOT OK</p>"
        else:
            content = "<p>PLACEHOLDER</p>"

        # Create mailing template
        template = MailingTemplate(name=f"T_{mailing_title}", html=content)
        template.save()

        # Start sending tomorrow
        send_after = now()
        send_after = send_after + timedelta(days=1)
        send_after = send_after.replace(hour=3, minute=0, second=0)

        day_of_week = now().weekday()

        campaign = MailingCampaign(
            webinar=webinar,
            title=mailing_title,
            smtp_sender=smtp_sender,
            subjects=subjects,
            target_code=target_code,
            alias=alias,
            template=template,
            resignation_list=resignation_list,
            status=MailingCampaignStatus.SENDING,
            allowed_to_send_after=time(5, (10 * ((day_of_week + 1) % 7)) % 60, 0, 0),
            allowed_to_send_before=time(16, 0, 0, 0),
            send_after=send_after,
            is_main_campaign=True,
        )
        campaign.save()

        return redirect(
            reverse("core:crm_mailing_campaign_detail", kwargs={"pk": campaign.pk})
        )

    return TemplateResponse(
        request,
        template_name,
        {"webinar": webinar, "smtp_senders": smtp_senders, **form_data},
    )
