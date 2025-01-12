# flake8: noqa=E501

from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

from core.models import Webinar
from core.services.lecturer import LecturerService
from core.services.webinar import WebinarService


def webinar_price_and_invoice_page(request, slug: str):
    """Webinar page - price and invoice tab"""

    return HttpResponsePermanentRedirect(
        reverse("core:webinar_program_page", kwargs={"slug": slug})
    )

    template_name = "geeks/pages/webinar/WebinarPriceAndInvoicePage.html"
    webinar = get_object_or_404(Webinar, slug=slug)
    webinar_service = WebinarService(webinar)
    lecturer_service = LecturerService(webinar.lecturer)

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "CANONICAL": reverse(
                "core:webinar_price_and_invoice_page", kwargs={"slug": webinar.slug}
            ),
            "related_webinars": webinar_service.get_related_webinars(),
            "webinar_tabs": webinar_service.get_webinar_tabs(1),
            "lecturer_service": lecturer_service,
        },
    )
