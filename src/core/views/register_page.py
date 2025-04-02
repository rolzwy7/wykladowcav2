# flake8: noqa:E501
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import RegistrationForm
from core.models import WebinarRecordingToken
from core.services import RegistrationService


def register_page(request: HttpRequest):
    """Register page"""
    template_name = "geeks/pages/registration/RegisterPage.html"

    # If user is already authenticated redirect to list of webinar categories
    if request.user.is_authenticated:
        return redirect(
            reverse("core:webinar_category_page", kwargs={"slug": "wszystkie"})
        )

    # If recording token is set try to get participant
    recording_token = request.GET.get("ruuid", "")
    if recording_token:
        token_exists = WebinarRecordingToken.manager.filter(
            token=recording_token
        ).exists()
        if token_exists:
            recording_token = WebinarRecordingToken.manager.get(token=recording_token)
            participant = recording_token.participant
        else:
            return redirect(reverse("core:register_page"))
    else:
        participant = None

    # Handle POST request
    if request.method == POST:

        return HttpResponse("Cloudflare protection", status=200)

        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data["password1"]

            registration_service = RegistrationService(email, password1)
            user = registration_service.create_user(first_name, last_name)

            # Simplified registration
            if participant:
                webpath = reverse(
                    "core:recording_token_page", kwargs={"uuid": recording_token}
                )
                user.is_active = True
                user.save()
                login(request, user)
                return redirect(webpath)
            else:
                registration_service.send_confirmation_email(str(user.activation_token))
                webpath = reverse("core:register_info_page")
                return redirect(f"{webpath}?email={email}")

    else:
        if participant:
            form = RegistrationForm(
                initial={
                    "first_name": participant.first_name,
                    "last_name": participant.last_name,
                    "email": participant.email,
                }
            )
        else:
            form = RegistrationForm()

    return TemplateResponse(
        request,
        template_name,
        {"form": form, "participant": participant, "recording_token": recording_token},
    )


def register_info_page(request: HttpRequest):
    """Register info page"""
    template_name = "geeks/pages/registration/RegisterInfoPage.html"
    email = request.GET.get("email", "")
    return TemplateResponse(
        request,
        template_name,
        {"email": email},
    )


def register_activation_page(request: HttpRequest, activation_token: str):
    """Register activation page"""
    template_name = "geeks/pages/registration/RegisterActivationPage.html"
    RegistrationService.activate_user_by_activation_token(activation_token)
    user = RegistrationService.get_user_by_activation_token(activation_token)
    login(request, user)
    return TemplateResponse(
        request,
        template_name,
        {},
    )
