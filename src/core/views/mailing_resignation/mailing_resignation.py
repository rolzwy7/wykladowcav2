from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.services.mailing import MailingResignationService


def mailing_resignation_page(request: HttpRequest, resignation_code: str):
    """Mailing resignation page"""
    template_name = "core/pages/mailing_resignation/MailingResignationPage.html"
    service = MailingResignationService()

    resignation = service.get_by_resignation_code(resignation_code)

    if not resignation:
        return HttpResponse("Niepoprawny kod rezygnacji")

    if request.method == POST:
        service.confirm_resignation_by_code(resignation_code)
        return redirect(
            reverse(
                "core:mailing_resignation_page",
                kwargs={"resignation_code": resignation_code},
            )
        )

    return TemplateResponse(
        request,
        template_name,
        {
            "resignation_code": resignation_code,
            "confirmed": resignation.confirmed,
        },
    )
