"""ServiceOfferApplicationsListPage"""

# flake8: noqa=E501

from django.template.response import TemplateResponse

from core.models import ServiceOfferApplication
from core.models.enums import ServiceOfferApplicationStatus


def service_offer_applications_list_page(request):
    """service_offer_applications_list_page"""
    template_name = "core/pages/crm/service_offer/ServiceOfferApplicationsListPage.html"

    if request.GET.get("show_all"):
        service_offers = ServiceOfferApplication.manager.all().order_by("-created_at")
    else:
        service_offers = ServiceOfferApplication.manager.exclude(
            status=ServiceOfferApplicationStatus.PAID
        ).order_by("-created_at")

    return TemplateResponse(
        request,
        template_name,
        {"service_offers": service_offers},
    )
