from django.http import HttpRequest
from django.template.response import TemplateResponse

from core.models import CrmCompany


def htmx_crm_check_nip(request: HttpRequest, nip: str):
    """CRM check nip"""
    template_path = "htmx/htmx_crm_check_nip.html"

    # Get company
    try:
        company = CrmCompany.objects.get(nip=nip)
    except CrmCompany.DoesNotExist:
        company = None

    return TemplateResponse(
        request,
        template_path,
        {
            "nip": nip,
            "company": company,
        },
    )
