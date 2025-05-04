"""
Applications participants form step
"""

# flake8: noqa=E501

from django.db import transaction
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts.requests_consts import POST
from core.forms import SaleRecordingApplicationParticipantForm
from core.models import SaleRecordingApplication, SaleRecordingParticipant, Webinar
from core.services import ApplicationFormService


def sale_recording_application_participants_page(request, uuid: str):
    """Application participants page"""

    template_name = (
        "geeks/pages/sale_recording_application/ApplicationParticipantsPage.html"
    )
    application = get_object_or_404(SaleRecordingApplication, uuid=uuid)
    webinar: Webinar = application.sale_recording.recording.webinar
    participants = SaleRecordingParticipant.manager.filter(application=application)

    # Already saved participants
    data = [
        {
            "application": participant.application,
            "first_name": participant.first_name,
            "last_name": participant.last_name,
            "email": participant.email,
            "access_from": participant.access_from,
        }
        for participant in participants
    ]

    ApplicationParticipantsFormSet = formset_factory(
        SaleRecordingApplicationParticipantForm,  # type: ignore
        min_num=1,
        validate_min=True,
        max_num=10,
        validate_max=True,
        extra=0,
    )

    if request.method == POST:
        success, msg, request = ApplicationFormService.transform_post_data(request)
        formset = ApplicationParticipantsFormSet(request.POST, initial=data)  # type: ignore

        if not success:
            return TemplateResponse(
                request,
                template_name,
                {
                    "step_number": 2,
                    "step_title": "Ilość dostępów do nagrania",
                    "step_description": "Dodaj osoby, do których zostanie wysłany link z dostępem do nagrania ze szkolenia",
                    "application": application,
                    "webinar": webinar,
                    "formset": formset,
                    "transform_error_msg": msg,
                },
            )

        if formset.is_valid():
            with transaction.atomic():
                # Delete all current participants
                participants.delete()
                # Save new participants
                for form in formset.forms:
                    participant = form.save(commit=False)
                    participant.application = application
                    participant.save()
                # Mark application's participants step as finished
                application.save()

            return redirect(
                reverse(
                    "core:sale_recording_application_invoice_page",
                    kwargs={"uuid": application.uuid},
                )
            )
    else:
        formset = ApplicationParticipantsFormSet(initial=data)  # type: ignore

    return TemplateResponse(
        request,
        template_name,
        {
            "step_number": 2,
            "step_title": "Ilość dostępów do nagrania",
            "step_description": "Dodaj osoby, do których zostanie wysłany link z dostępem do nagrania ze szkolenia",
            "formset": formset,
            "application": application,
            "webinar": webinar,
        },
        # {"formset": formset, **service.get_context()},
    )
