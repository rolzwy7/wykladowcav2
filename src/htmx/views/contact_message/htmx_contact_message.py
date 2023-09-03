from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest
from django.template.response import TemplateResponse

from core.consts import POST, TelegramChats
from core.forms import ContactMessageForm
from core.services import TelegramService

EMAIL_OFFICE = settings.COMPANY_OFFICE_EMAIL


def htmx_contact_message(request: HttpRequest):
    """Toggle CRM participant phoned"""
    template_path = "htmx/htmx_contact_message_form.html"

    related_to = request.GET.get("related_to", "")

    if request.method == POST:
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            contact_message_id: int = contact_msg.id
            fullname = f"{contact_msg.first_name} {contact_msg.last_name}"
            phone_number = contact_msg.phone_number

            # TODO: Move this to Celery !
            telegram_service = TelegramService()
            telegram_service.send_chat_message(
                "Wysłano pytanie sprawdź CRM / Skrzynke e-mail",
                TelegramChats.OTHER,
            )

            # TODO: Move this to Celery !
            body = f"""
            \rZadano pytanie:
            \r
            \r{fullname}
            \rEmail: {contact_msg.email}
            \rTelefon: {phone_number if phone_number else "Nie podano"}
            \rStrona: {contact_msg.related_to}
            \r
            \rTreść pytania: ```
            \r{contact_msg.message}
            ```
            """
            email_message = EmailMultiAlternatives(
                subject=f"Zadano pytanie #{contact_message_id} - {fullname}",
                body=body,
                from_email=f"{settings.COMPANY_NAME} <{EMAIL_OFFICE}>",
                to=[EMAIL_OFFICE],
                headers={"Organization": settings.COMPANY_NAME_FULL},
                reply_to=[contact_msg.email],
            )
            email_message.send()

            return TemplateResponse(
                request,
                "htmx/htmx_contact_message_form_success.html",
                {},
            )
    else:
        form = ContactMessageForm(initial={"related_to": related_to})

    return TemplateResponse(
        request,
        template_path,
        {"form": form},
    )
