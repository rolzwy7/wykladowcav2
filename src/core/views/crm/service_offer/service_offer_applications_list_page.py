"""ServiceOfferApplicationsListPage"""

# flake8: noqa=E501

from django import forms
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import ServiceOffer, ServiceOfferApplication

# from core.models.enums import ServiceOfferApplicationStatus


class ServiceOfferApplicationStatusForm(forms.ModelForm):
    """ServiceOfferApplicationStatusForm"""

    class Meta:
        """Meta"""

        model = ServiceOfferApplication
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
        }


def service_offer_applications_list_page(request):
    """service_offer_applications_list_page"""

    service_slug = request.GET.get("usluga")
    status = request.GET.get("status")

    if not service_slug:
        service_offers = ServiceOffer.manager.all()
        return TemplateResponse(
            request,
            "core/pages/crm/service_offer/ServiceOfferListPage.html",
            {
                "service_offers": service_offers,
                "statuses": [
                    (
                        status,
                        status_display,
                        ServiceOfferApplication.manager.filter(status=status).count(),
                    )
                    for status, status_display in ServiceOfferApplication.STATUS
                ],
            },
        )

    service_offer = get_object_or_404(ServiceOffer, slug=service_slug)

    service_offer_applications = ServiceOfferApplication.manager.filter(
        service_offer__slug=service_slug
    ).order_by("-created_at")

    if status:
        service_offer_applications = service_offer_applications.filter(status=status)
        status_display = {
            _status: _status_disp
            for _status, _status_disp in ServiceOfferApplication.STATUS
        }[status]
    else:
        status_display = None

    return TemplateResponse(
        request,
        "core/pages/crm/service_offer/ServiceOfferApplicationsListPage.html",
        {
            "service_offer": service_offer,
            "service_offer_applications": service_offer_applications,
            "service_slug": service_slug,
            "status_display": status_display,
        },
    )
