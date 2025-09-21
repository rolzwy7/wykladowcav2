"""Mailing test e-mail"""

# flake8: noqa=E501

from django.conf import settings
from django.urls import reverse

from core.libs.mailing.title_test import get_or_create_mailing_title_test
from core.models import MailingCampaign, MailingTemplate
from core.services import SenderSmtpService
from core.services.mailing import MailingResignationService, MailingTrackingService

BASE_URL = settings.BASE_URL


def send_campaign_test_email(email: str, mailing_campaign: MailingCampaign):
    """send_campaign_test_email"""

    campaign_id: int = mailing_campaign.id  # type: ignore
    service = SenderSmtpService(mailing_campaign.smtp_sender)

    template: MailingTemplate = mailing_campaign.template

    resignation_code = MailingResignationService.get_or_create_inactive_resignation(
        email, mailing_campaign.resignation_list
    )
    resignation_path = reverse(
        "core:mailing_resignation_page_with_list",
        kwargs={
            "resignation_code": resignation_code,
            "resignation_list": mailing_campaign.resignation_list,
        },
    )
    resignation_url = BASE_URL + resignation_path
    tracking_code = MailingTrackingService.get_or_create_tracking(email)
    subject = f"[PRÓBA] {mailing_campaign.get_random_subject()}"

    test_title = get_or_create_mailing_title_test(subject, str(campaign_id))

    with service.get_smtp_connection() as connection:
        service.send_email(
            connection=connection,
            email=email,
            alias=mailing_campaign.alias,
            subject=subject,
            html=template.html,
            text=template.text,
            resignation_url=resignation_url,
            resignation_path=resignation_path,
            tracking_code=tracking_code,
            campaign_id=campaign_id,
            test_subject_id=str(test_title.id),  # type: ignore
        )
