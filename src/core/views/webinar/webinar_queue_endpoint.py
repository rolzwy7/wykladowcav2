"""Webinar Queue Endpoint"""

# flake8: noqa=E501

from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from core.consts import TelegramChats
from core.consts.requests_consts import POST
from core.libs.spy import create_spy_object
from core.models import WebinarAggregate, WebinarQueue
from core.services import LeadService, TelegramService


def webinar_queue_endpoint(request: HttpRequest, grouping_token: str):
    """webinar_queue_endpoint"""
    aggregate = get_object_or_404(WebinarAggregate, grouping_token=grouping_token)

    if request.method == POST:
        email = request.POST["email"]
        phone = request.POST["phone"]

        # Create webinar queue object
        with transaction.atomic():

            spy_object = create_spy_object(request, "AGGREGATE_NO_WEBINARS_FORM_SUBMIT")

            webinar_queue = WebinarQueue(
                email=email,
                phone=phone,
                aggregate=aggregate,
                aggregate_current_title=aggregate.title,
                spy_object=spy_object,
            )
            webinar_queue.save()

        telegram_service = TelegramService()
        telegram_service.try_send_chat_message(
            f"🏆 AGREGAT LEAD KOLEJKA: {email} - {aggregate.title}",
            TelegramChats.OTHER,
        )

    return redirect(
        reverse("core:thanks_page", kwargs={"choice_slug": "przypomnij-o-terminie"})
    )
