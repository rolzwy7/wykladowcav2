from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import ResignationForm
from core.services.mailing import MailingResignationService


def mailing_resignation_by_form_page(request: HttpRequest):
    """Mailing resignation by form page"""
    template_name = (
        "core/pages/mailing_resignation/MailingResignationByFormPage.html"
    )

    if request.method == POST:
        form = ResignationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            code = MailingResignationService.get_or_create_inactive_resignation(
                email
            )
            MailingResignationService.confirm_resignation_by_email(email)
            MailingResignationService.mark_resignation_as_manual(email)
            return redirect(
                reverse(
                    "core:mailing_resignation_page",
                    kwargs={"resignation_code": code},
                )
            )
    else:
        form = ResignationForm()

    return TemplateResponse(
        request,
        template_name,
        {"form": form},
    )


def mailing_resignation_by_code_page(
    request: HttpRequest, resignation_code: str
):
    """Mailing resignation page"""
    template_name = (
        "core/pages/mailing_resignation/MailingResignationByCodePage.html"
    )

    resignation = MailingResignationService.get_by_resignation_code(
        resignation_code
    )

    if not resignation:
        return HttpResponse("Niepoprawny kod rezygnacji")

    if request.method == POST:
        MailingResignationService.confirm_resignation_by_code(resignation_code)
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
