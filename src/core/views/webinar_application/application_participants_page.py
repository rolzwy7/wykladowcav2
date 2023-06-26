from django.db import transaction
from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts.requests_consts import POST
from core.forms import ApplicationParticipantForm
from core.models import WebinarApplication, WebinarParticipant
from core.models.enums import WebinarApplicationStep
from core.services import ApplicationFormService


def application_participants_page(request, uuid: str):
    """Application participants page"""
    template_name = "core/pages/application/ApplicationParticipantsPage.html"
    application = get_object_or_404(WebinarApplication, uuid=uuid)
    webinar = application.webinar
    participants = WebinarParticipant.objects.filter(application=application)
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
        max_num=10,
        validate_max=True,
        extra=0,
    )

    if request.method == POST:
        request = ApplicationFormService.transform_post_data(request)
        formset = ApplicationParticipantsFormSet(request.POST, initial=data)
        if formset.is_valid():
            with transaction.atomic():
                # Delete all current participants
                participants.delete()

                # Save new participants
                for form in formset.forms:
                    participant = WebinarParticipant(
                        application=application,
                        first_name=form.cleaned_data["first_name"],
                        last_name=form.cleaned_data["last_name"],
                        email=form.cleaned_data["email"],
                        phone=form.cleaned_data["phone"],
                    )
                    participant.save()

            return service.get_next_step_redirect()
    else:
        formset = ApplicationParticipantsFormSet(initial=data)

    return TemplateResponse(
        request,
        template_name,
        {"formset": formset, **service.get_context()},
    )
