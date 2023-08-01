from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.models import (
    WebinarApplication,
    WebinarMoveRegister,
    WebinarMoveRegisterItem,
)
from core.models.enums import ApplicationMoveStatus, ApplicationStatus

# TODO: DRY


def webinar_moving_accept_page(request: HttpRequest, token: str):
    """Webinar moving accept page"""
    template_name = "core/pages/webinar_move/WebinarMoveAcceptPage.html"
    move_register_item = get_object_or_404(WebinarMoveRegisterItem, token=token)
    move_register: WebinarMoveRegister = move_register_item.move_register
    application: WebinarApplication = move_register_item.application

    # Redirect to thanks page if already answered
    if move_register_item.status != ApplicationMoveStatus.INIT:
        return redirect(
            reverse("core:webinar_moving_thanks_page", kwargs={"token": token})
        )

    # Mark as clicked
    if move_register_item.clicked_accept_link is False:
        move_register_item.clicked_accept_link = True
        move_register_item.save()

    # On form submit mark as `ACCEPTED`
    if request.method == POST:
        move_register_item.status = ApplicationMoveStatus.ACCEPTED
        move_register_item.save()
        return redirect(
            reverse("core:webinar_moving_thanks_page", kwargs={"token": token})
        )

    return TemplateResponse(
        request,
        template_name,
        {
            "token": token,
            "move_register": move_register,
        },
    )
