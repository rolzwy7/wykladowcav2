"""
Applications participants form step
"""

# flake8: noqa=E501

from django.db import transaction
from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.timezone import now

from core.consts.requests_consts import POST
from core.forms import ApplicationParticipantForm
from core.models import Webinar, WebinarApplication, WebinarParticipant
from core.models.enums import WebinarApplicationStep
from core.services import ApplicationFormService


def application_participants_page(request, uuid: str):
    """Application participants page"""
    template_name = "geeks/pages/application/ApplicationParticipantsPage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar: Webinar = application.webinar
    participants = WebinarParticipant.manager.filter(application=application)
    service = ApplicationFormService(
        webinar, application, WebinarApplicationStep.PARTICIPANTS
    )
    service.redirect_on_application_error()

    # Already saved participants
    data = [
        {
            "application": participant.application,
            "first_name": participant.first_name,
            "last_name": participant.last_name,
            "email": participant.email,
            "phone": participant.phone,
        }
        for participant in participants
    ]

    ApplicationParticipantsFormSet = formset_factory(
        ApplicationParticipantForm,
        min_num=1,
        validate_min=True,
        max_num=20,
        validate_max=True,
        extra=0,
    )

    if request.method == POST:
        success, msg, request = ApplicationFormService.transform_post_data(request)
        formset = ApplicationParticipantsFormSet(request.POST, initial=data)

        if not success:
            return TemplateResponse(
                request,
                template_name,
                {
                    "formset": formset,
                    **service.get_context(),
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
                application.step_participants_finished = True
                application.step_dt_participants_end = now()
                application.save()

            return service.get_next_step_redirect()
    else:
        formset = ApplicationParticipantsFormSet(initial=data)
        if not application.step_dt_participants_start:
            application.step_dt_participants_start = now()
            application.save()

    return TemplateResponse(
        request,
        template_name,
        {"formset": formset, **service.get_context()},
    )
