from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.timezone import datetime

from core.consts import POST
from core.forms.crm import CrmMoveActionForm
from core.models import Webinar
from core.models.enums import WebinarStatus

# from core.services.webinar.crm import WebinarMovingService
from core.tasks_dispatch import after_webinar_moved_dispatch


def move_webinar_action(request: HttpRequest, pk: int):
    """Move webinar action page controller"""
    template_name = "core/pages/crm/webinar_actions/CrmWebinarMoveAction.html"
    webinar = get_object_or_404(Webinar, pk=pk)
    # moving_service = WebinarMovingService(webinar)

    if webinar.status != WebinarStatus.INIT:
        return HttpResponse("Cannot move webinar which is not in `INIT` status")

    if request.method == POST:
        form = CrmMoveActionForm(request.POST)
        if form.is_valid():
            new_date: datetime = form.cleaned_data["new_date"]
            # TODO: new_date can't be less then webinar date
            after_webinar_moved_dispatch(webinar, new_date)
    else:
        form = CrmMoveActionForm()

    return TemplateResponse(
        request,
        template_name,
        {"webinar": webinar, "form": form},
    )
