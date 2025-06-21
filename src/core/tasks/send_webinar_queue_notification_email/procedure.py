# flake8: noqa:E501
# pylint: disable=line-too-long
import json

from django.conf import settings
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.libs.html_operations.html_to_text import html_to_text
from core.libs.html_operations.minify_html import op_minify_html
from core.models import SmtpSender
from core.services import SenderSmtpService


class SendWebinarQueueNotificationEmailParams(BaseModel):
    """Params"""

    email: str
    smtp_sender_id: int
    email_alias: str
    subject: str
    email_content: str


def params(
    email: str, smtp_sender_id: int, email_alias: str, subject: str, email_content: str
) -> str:
    """Create params"""
    json_dump = json.dumps(
        SendWebinarQueueNotificationEmailParams(
            email=email,
            smtp_sender_id=smtp_sender_id,
            email_alias=email_alias,
            subject=subject,
            email_content=email_content,
        ).dict()
    )
    return json_dump


def send_webinar_queue_notification_email(
    procedure_params: SendWebinarQueueNotificationEmailParams,
):
    """send_webinar_queue_notification_email"""

    smtp_sender = SmtpSender.objects.get(id=procedure_params.smtp_sender_id)

    smtp_service = SenderSmtpService(smtp_sender)
    connection = smtp_service.get_smtp_connection()

    html = procedure_params.email_content
    text = html_to_text(op_minify_html(html))

    smtp_service.send_email(
        connection=connection,
        email=procedure_params.email,
        alias=procedure_params.email_alias,
        subject=procedure_params.subject,
        html=html,
        text=text,
        resignation_url="",
        tracking_code="",
        campaign_id=0,
        cc=settings.COMPANY_OFFICE_EMAIL,
    )

    try:
        connection.close()  # close SMTP connection
    except Exception as e:
        pass
