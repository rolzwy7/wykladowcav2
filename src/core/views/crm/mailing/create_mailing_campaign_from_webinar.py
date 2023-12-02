import requests
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import now

from core.consts.requests_consts import POST
from core.models import MailingCampaign, MailingTemplate, SmtpSender, Webinar


def create_mailing_campaign_from_webinar(request, pk: int):
    """create_mailing_campaign_from_webinar"""
    template_name = "core/pages/crm/mailing/MailingCreateFromWebinar.html"
    webinar = get_object_or_404(Webinar, pk=pk)
    smtp_senders = SmtpSender.objects.all()

    if request.method == POST:
        content_url = request.POST.get("content_url", "")
        smpt_sender_id = request.POST.get("smpt_sender_id")

        smtp_sender = SmtpSender.objects.get(id=int(smpt_sender_id))
        campaign_title = f"{now().strftime('%Y%m%d')}_{webinar.title[:30]}"

        if content_url:
            result = requests.get(content_url)
            if not result.ok:
                content = "<p>RESULT NOT OK</p>"
            else:
                content = str(result.content, "utf8")
        else:
            content = "<p>PLACEHOLDER</p>"

        template = MailingTemplate(name=campaign_title, html=content)
        template.save()

        campaign = MailingCampaign(
            webinar=webinar,
            title=campaign_title,
            smtp_sender=smtp_sender,
            subjects=webinar.title,
            alias=webinar.lecturer.fullname,
            template=template,
        )
        campaign.save()

        return redirect(
            reverse("core:crm_mailing_campaign_detail", kwargs={"pk": campaign.pk})
        )

    return TemplateResponse(
        request, template_name, {"webinar": webinar, "smtp_senders": smtp_senders}
    )
