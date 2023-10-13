from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import WebinarMoveRegister, WebinarMoveRegisterItem


def webinar_moving_thanks_page(request: HttpRequest, token: str):
    """Webinar moving accept page"""
    template_name = "core/pages/webinar_move/WebinarMoveThanksPage.html"
    move_register_item = get_object_or_404(WebinarMoveRegisterItem, token=token)
    move_register: WebinarMoveRegister = move_register_item.move_register

    return TemplateResponse(
        request,
        template_name,
        {
            "token": token,
            "move_register": move_register,
        },
    )
