# flake8: noqa=E501

from django.db.models import Q
from django.template.response import TemplateResponse

from core.models import WebinarApplicationMetadata


def crm_invoices_list(request):
    """CRM Invoices List"""
    template_name = "core/pages/crm/invoices/InvoicesList.html"
    meta_applications = WebinarApplicationMetadata.objects.filter(
        ~Q(invoice_number="")
    ).order_by("-application__webinar__date")
    return TemplateResponse(
        request,
        template_name,
        {"meta_applications": meta_applications},
    )
