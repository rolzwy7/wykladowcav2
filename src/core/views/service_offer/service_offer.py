"""Service Offer Page"""

# flake8: noqa=E501

from django.forms import EmailInput, FileInput, ModelForm, Textarea, TextInput
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import ServiceOffer, ServiceOfferApplication


class ServiceOfferApplicationForm(ModelForm):
    """ServiceOfferApplicationForm"""

    class Meta:
        model = ServiceOfferApplication
        fields = [
            "nip",
            "name",
            "address",
            "postal_code",
            "city",
            "first_name",
            "last_name",
            "email_contact",
            "email_confirmation",
            "phone",
            "file",
            "additional_info",
        ]
        widgets = {
            "nip": TextInput(attrs={"class": "form-control"}),
            "name": TextInput(attrs={"class": "form-control"}),
            "address": TextInput(attrs={"class": "form-control"}),
            "postal_code": TextInput(attrs={"class": "form-control"}),
            "city": TextInput(attrs={"class": "form-control"}),
            "first_name": TextInput(attrs={"class": "form-control"}),
            "last_name": TextInput(attrs={"class": "form-control"}),
            "email_contact": EmailInput(attrs={"class": "form-control"}),
            "email_confirmation": EmailInput(attrs={"class": "form-control"}),
            "phone": TextInput(attrs={"class": "form-control"}),
            "file": FileInput(attrs={"class": "form-control"}),
            "additional_info": Textarea(
                attrs={"class": "form-control", "cols": "40", "rows": "3"}
            ),
        }


def service_offer_page(request, slug: str):
    """Service offer page"""
    template_name = "geeks/pages/service_offer/ServiceOfferPage.html"
    service_offer = get_object_or_404(ServiceOffer, slug=slug)
    form = ServiceOfferApplicationForm()

    return TemplateResponse(
        request,
        template_name,
        {
            "hide_footer_newsletter_singup": True,
            "service_offer": service_offer,
            "form": form,
            "slug": slug,
        },
    )
