from django.http import HttpRequest
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import RegistrationForm
from core.services import RegistrationService


def register_page(request: HttpRequest):
    """Register page"""
    template_name = "core/pages/registration/RegisterPage.html"

    if request.user.is_authenticated:
        return redirect(
            reverse("core:webinar_category_page", kwargs={"slug": "wszystkie"})
        )

    if request.method == POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            a = 1
            # first_name = form.cleaned_data["first_name"]
            # last_name = form.cleaned_data["last_name"]
            # email = form.cleaned_data["email"]
            # password1 = form.cleaned_data["password1"]

            # registration_service = RegistrationService(email, password1)
            # user = registration_service.create_user(first_name, last_name)
            # registration_service.send_confirmation_email(
            #     str(user.activation_token)
            # )
    else:
        form = RegistrationForm()

    return TemplateResponse(
        request,
        template_name,
        {"form": form},
    )


def register_info_page(request: HttpRequest):
    """Register info page"""
    template_name = "core/pages/registration/RegisterInfoPage.html"
    return TemplateResponse(
        request,
        template_name,
        {},
    )


def register_activation_page(request: HttpRequest, activation_token: str):
    """Register activation page"""
    template_name = "core/pages/registration/RegisterActivationPage.html"
    # RegistrationService.activate_user_by_activation_token(activation_token) TODO
    return TemplateResponse(
        request,
        template_name,
        {},
    )
