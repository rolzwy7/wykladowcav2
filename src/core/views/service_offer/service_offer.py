"""Service Offer Page"""

# flake8: noqa=E501

from django.core.exceptions import ValidationError
from django.forms import (
    CheckboxInput,
    EmailInput,
    FileInput,
    ModelForm,
    Textarea,
    TextInput,
)
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts.requests_consts import POST
from core.models import ServiceOffer, ServiceOfferApplication
from core.tasks_dispatch import after_service_offer_sent


class ServiceOfferApplicationForm(ModelForm):
    """ServiceOfferApplicationForm"""

    def clean_accepted_rodo(self):
        data = self.cleaned_data["accepted_rodo"]
        if data is not True:
            raise ValidationError("Zaakceptuj oświadczenie o przetwarzaniu danych")
        return data

    def clean_accepted_terms(self):
        data = self.cleaned_data["accepted_terms"]
        if data is not True:
            raise ValidationError("Zaakceptuj oświadczenie o regulaminie")
        return data

    # def clean_file(self):
    #     data = self.cleaned_data["file"]
    #     if data is None:
    #         raise ValidationError("Prześlij załącznik w swoim zapytaniu")
    #     return data

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
            "accepted_rodo",
            "accepted_terms",
        ]
        widgets = {
            "nip": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Numer NIP, np. 774-00-01-454",
                }
            ),
            "name": TextInput(
                attrs={"class": "form-control", "placeholder": "Nazwa placówki / firmy"}
            ),
            "address": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ulica i numer lokalu, np. Przemysłowa 10A",
                }
            ),
            "postal_code": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Kod pocztowy, np. 45-573",
                }
            ),
            "city": TextInput(
                attrs={"class": "form-control", "placeholder": "Miasto, np. Warszawa"}
            ),
            "first_name": TextInput(attrs={"class": "form-control"}),
            "last_name": TextInput(attrs={"class": "form-control"}),
            "email_contact": EmailInput(attrs={"class": "form-control"}),
            # "email_confirmation": EmailInput(attrs={"class": "form-control"}),
            "file": FileInput(attrs={"class": "form-control"}),
            "phone": TextInput(attrs={"class": "form-control"}),
            "additional_info": Textarea(
                attrs={"class": "form-control", "cols": "40", "rows": "3"}
            ),
            "accepted_rodo": CheckboxInput(attrs={"class": "form-check-input"}),
            "accepted_terms": CheckboxInput(attrs={"class": "form-check-input"}),
        }


def service_offer_page(request, slug: str):
    """Service offer page"""
    template_name = "geeks/pages/service_offer/ServiceOfferPage.html"
    service_offer = get_object_or_404(ServiceOffer, slug=slug)
    hide_intro = request.GET.get("h")

    if request.method == POST:
        form = ServiceOfferApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application: ServiceOfferApplication = form.save(commit=False)
            application.service_offer = service_offer
            application.save()
            after_service_offer_sent(service_offer, application)
            return redirect(
                reverse(
                    "core:service_offer_thanks_page",
                    kwargs={"slug": service_offer.slug},
                )
            )
    else:
        form = ServiceOfferApplicationForm()

    return TemplateResponse(
        request,
        template_name,
        {
            "hide_footer_newsletter_singup": True,
            "hide_intro": hide_intro,
            "service_offer": service_offer,
            "form": form,
            "slug": slug,
        },
    )


def service_offer_thanks_page(request, slug: str):
    """Service offer page"""
    template_name = "geeks/pages/service_offer/ServiceOfferThanksPage.html"
    service_offer = get_object_or_404(ServiceOffer, slug=slug)

    return TemplateResponse(
        request,
        template_name,
        {
            "hide_footer_newsletter_singup": True,
            "service_offer": service_offer,
        },
    )
