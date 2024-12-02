"""ServiceOfferApplicationsListPage"""

# flake8: noqa=E501

from django.template.response import TemplateResponse

from core.models import ServiceOffer, ServiceOfferApplication

# from core.models.enums import ServiceOfferApplicationStatus


def service_offer_applications_list_page(request):
    """service_offer_applications_list_page"""
    template_name = "core/pages/crm/service_offer/ServiceOfferApplicationsListPage.html"

    service_slug = request.GET.get("usluga")

    if not service_slug:
        template_name = "core/pages/crm/service_offer/ServiceOfferListPage.html"
        service_offers = ServiceOffer.manager.all()
        return TemplateResponse(
            request,
            template_name,
            {"service_offers": service_offers},
        )

    if service_slug:
        service_offers = ServiceOfferApplication.manager.filter(
            service_offer__slug=service_slug
        ).order_by("-created_at")
    else:
        service_offers = ServiceOfferApplication.manager.all().order_by("-created_at")

    # if request.GET.get("show_all"):
    # else:
    #     service_offers = ServiceOfferApplication.manager.exclude(
    #         status=ServiceOfferApplicationStatus.PAID
    #     ).order_by("-created_at")

    return TemplateResponse(
        request,
        template_name,
        {"service_offers": service_offers, "service_slug": service_slug},
    )
