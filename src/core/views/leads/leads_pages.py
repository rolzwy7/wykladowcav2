from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from core.consts import TelegramChats
from core.consts.requests_consts import POST
from core.models import Webinar, WebinarCategory
from core.models.enums import LeadSource
from core.services import LeadService, TelegramService


def lead_footer_post_endpoint(request: HttpRequest):
    """lead_footer_post_endpoint"""

    if request.method == POST:
        email = request.POST["email"]

        # Get or create lead object
        lead = LeadService.get_or_create_lead(
            email, LeadSource.NEWSLETTER_FOOTER, request=request
        )

        # Try to save category if set
        category_id = request.POST.get("category", "0")
        if category_id != "0":
            category = WebinarCategory.manager.get(id=int(category_id))
            lead.preferences.add(category)

    return redirect(reverse("core:leads_thanks_page"))


def lead_webinar_post_endpoint(request: HttpRequest, pk: int):
    """lead_webinar_post_endpoint"""
    webinar = get_object_or_404(Webinar, pk=pk)

    if request.method == POST:
        email = request.POST["email"]

        # Get or create lead object
        LeadService.get_or_create_lead(
            email,
            LeadSource.ARCHIVED_WEBINAR,
            request=request,
            categories=[_ for _ in webinar.categories.all()],
        )

        telegram_service = TelegramService()
        telegram_service.try_send_chat_message(
            f"Lead: {email} - {webinar.title}",
            TelegramChats.OTHER,
        )

    return redirect(reverse("core:leads_thanks_page"))
