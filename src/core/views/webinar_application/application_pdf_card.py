from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page

from core.models import WebinarApplication
from core.services import ApplicationPdfCardService

COMPANY_NAME = settings.COMPANY_NAME


@cache_page(5)  # 5s
def application_pdf_card(request, uuid: str):
    """Controller for application PDF card rendering"""
    application = get_object_or_404(WebinarApplication, uuid=uuid)

    pdf_card_service = ApplicationPdfCardService(application)

    pdf_bytes = pdf_card_service.create_pdf().to_bytes()
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    filename = f"Karta Zgłoszeniowa - {COMPANY_NAME}"  # TODO: Why it's not working ?
    response["Content-Disposition"] = f'inline; filename="{filename}.pdf"'
    return response
