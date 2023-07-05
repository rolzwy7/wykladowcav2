from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts import POST
from core.forms import ApplicationTypeForm
from core.models import Webinar, WebinarApplication
from core.services import ApplicationFormService


def application_type_page(request, pk: int):
    """Controller for webinar application form page - application type form"""
    template_name = "core/pages/application/ApplicationTypePage.html"
    webinar = get_object_or_404(Webinar, pk=pk)

    if request.method == POST:
        form = ApplicationTypeForm(request.POST)
        if form.is_valid():
            application = WebinarApplication(
                application_type=form.cleaned_data["application_type"],
                price_netto=webinar.price,
                price_old=webinar.price_netto,
                webinar=webinar,
                discount_applied=webinar.is_discounted,
            )
            if request.user.is_authenticated:
                application.user = request.user
            application.save()
            return ApplicationFormService.get_application_type_redirect(
                application.application_type, application.uuid
            )
    else:
        form = ApplicationTypeForm()

    return TemplateResponse(
        request,
        template_name,
        {
            "step_number": "1",
            "step_title": "Typ zgłoszenia",
            "step_description": "Wybierz typ wysyłanego zgłoszenia",
            "application_timeline": [("Typ zgłoszenia", "-", True)],
            "webinar": webinar,
            "form": form,
        },
    )
