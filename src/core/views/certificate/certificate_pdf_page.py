from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from core.models import WebinarCertificate
from core.services import CertificateService


def certificate_pdf_page(request, uuid: str):
    """View certificate PDF"""
    certificate = get_object_or_404(WebinarCertificate, uuid=uuid)
    service = CertificateService(certificate)
    return HttpResponse(service.get_pdf_bytes(), content_type="application/pdf")
