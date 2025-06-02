"""Closed webinar contact page"""

# flake8: noqa=E501

from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import TelegramChats
from core.forms import ClosedWebinarContactForm
from core.models import ClosedWebinarContactMessage
from core.services import TelegramService


def closed_webinar_contact_page(request):
    """closed_webinar_contact_page"""

    template_name = "geeks/pages/ClosedWebinarContactPage.html"

    if request.method == "POST":
        form = ClosedWebinarContactForm(request.POST)
        if form.is_valid():
            contact_message: ClosedWebinarContactMessage = form.save(commit=False)
            tracking_code = request.session.get("tracking_code", "no_code")
            contact_message.tracking_info = tracking_code
            contact_message.save()
            telegram_service = TelegramService()
            telegram_service.send_chat_message(
                "Wysłano zapytanie o szkolenie zamknięte:\n\n"
                + contact_message.message,
                TelegramChats.OTHER,
            )
            return redirect(reverse("core:closed_webinar_contact_sent_page"))
    else:
        form = ClosedWebinarContactForm()

    return TemplateResponse(request, template_name, {"form": form})


def closed_webinar_contact_sent_page(request):
    """closed_webinar_contact_sent_page"""

    template_name = "geeks/pages/ClosedWebinarContactSentPage.html"

    return TemplateResponse(request, template_name, {})
