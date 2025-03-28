"""Certificate PDF page"""

# flake8: noqa=E501

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page

from core.models import WebinarCertificate
from core.services import CertificateService


@cache_page(15)  # 15s
def certificate_pdf_page(request, uuid: str):
    """View certificate PDF"""
    certificate = get_object_or_404(WebinarCertificate, uuid=uuid)
    service = CertificateService(certificate)
    response = HttpResponse(service.get_pdf_bytes(), content_type="application/pdf")
    filename = (
        f"Certyfikat"
        f" {certificate.first_name} {certificate.last_name}"
        f" - Wykladowca_pl"
    )
    response["Content-Disposition"] = f'inline; filename="{filename}.pdf"'
    return response
