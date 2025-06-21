"""CRM Send Webinar Queue Email Notifications"""

# flake8: noqa=E501

from celery import group
from django.conf import settings
from django.db.models import Q
from django.forms import CharField, Form, ModelChoiceField, Select, Textarea, TextInput
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import now

from core.consts import TelegramChats
from core.models import SmtpSender, WebinarAggregate, WebinarQueue
from core.services import TelegramService
from core.tasks import (
    params_send_webinar_queue_notification_email,
    task_send_webinar_queue_notification_email,
)

NOTIFICATION_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Template</title>
</head>
<body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #ffffff;">
    <div style="width: 100%; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center;">
            <h1>Wykładowca.pl</h1>
        </div>
        <div style="padding: 20px 0; line-height: 1.6;">
            <h2>Szanowni Państwo</h2>

            <p>Z przyjemnością informujemy, że szkolenie, którym są Państwo zainteresowani, jest ponownie dostępne w naszej ofercie.</p>

            <p>
                <b>{{TITLE}}</b>
            </p>

            <p>
            Zapraszamy do zapisów na stronie szkolenia: <br>
            <a href="{{URL}}">{{URL_TEXT}}</a>
            </p>
        </div>
        <div style="text-align: center; padding: 20px 0; font-size: 12px; color: #666666;">
            <p>
                Otrzymali Państwo tę wiadomość e-mail, ponieważ adres {{EMAIL}} został podany, jako adres do powiadomień w razie pojawienia się nowego terminu szkolenia: „{{TITLE}}”
            </p>
        </div>
    </div>
</body>
</html>
"""


class WebinarEmailNotificationForm(Form):
    """WebinarEmailNotificationForm"""

    smtp_sender_choice = ModelChoiceField(
        label="Konto wysyłkowe",
        queryset=SmtpSender.objects.all(),
        to_field_name="username",
        required=True,
        widget=Select(attrs={"class": "form-control"}),
    )
    sender_alias = CharField(
        label="Alias e-mail",
        max_length=100,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    subject = CharField(
        label="Tytuł e-mail",
        max_length=255,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    content = CharField(
        label="Wiadomość e-mail", widget=Textarea(attrs={"class": "form-control"})
    )


def crm_send_webinar_queue_email_notifications(request, grouping_token: str):
    """crm_send_webinar_queue_email_notifications"""

    template_name = "core/pages/crm/CrmSendWebinarQueueEmailNotifications.html"
    aggragate = get_object_or_404(WebinarAggregate, grouping_token=grouping_token)

    webinar_queue = WebinarQueue.manager.filter(
        Q(aggregate=aggragate) & Q(sent_notification=False)
    )

    if request.method == "POST":
        form = WebinarEmailNotificationForm(request.POST)
        if form.is_valid():
            # Smtp sender
            smtp_sender_choice = form.data["smtp_sender_choice"]
            smtp_sender = SmtpSender.objects.get(username=smtp_sender_choice)
            # Alias
            sender_alias = form.data["sender_alias"]
            # Subject
            subject = form.data["subject"]
            # Tasks list
            tasks = []

            for queue_elem in webinar_queue:

                # URL
                url_path = reverse(
                    "core:webinar_aggregate_page", kwargs={"slug": aggragate.slug}
                )
                url = f"{settings.COMPANY_WWW}{url_path}"

                # HTML
                html = form.data["content"]
                html = html.replace("{{TITLE}}", aggragate.title)
                html = html.replace("{{URL}}", url)
                html = html.replace("{{URL_TEXT}}", url)
                html = html.replace("{{EMAIL}}", queue_elem.email)

                tasks.append(
                    task_send_webinar_queue_notification_email.si(
                        params_send_webinar_queue_notification_email(
                            queue_elem.email,
                            smtp_sender.id,  # type: ignore
                            sender_alias,
                            subject,
                            html,
                        )
                    )
                )

            group(*tasks).apply_async()

            webinar_queue.update(sent_notification=True, sent_notification_at=now())

            telegram_service = TelegramService()
            telegram_service.try_send_chat_message(
                f"Kolejka: Wysłano powiadomienia o terminie - {subject}",
                TelegramChats.OTHER,
            )

            return redirect(reverse("core:crm_upcoming_webinars"))
    else:
        form = WebinarEmailNotificationForm(
            initial={
                "content": NOTIFICATION_HTML,
                "subject": f"Szkolenie jest już dostępne: {aggragate.title}",
            }
        )

    return TemplateResponse(
        request,
        template_name,
        {"webinar_queue": webinar_queue, "aggragate": aggragate, "form": form},
    )
