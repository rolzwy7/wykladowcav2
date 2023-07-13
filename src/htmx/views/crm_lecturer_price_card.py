from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.template.response import TemplateResponse

from core.consts import POST
from core.forms.crm import CrmLecturerPriceCardForm
from core.models import Webinar, WebinarMetadata
from core.services import CrmWebinarService


def crm_lecturer_price_card(request: HttpRequest, webinar_pk: int, mode: str):
    """CRM lecturer price card"""
    result_template_path = "htmx/lecturer_price_card.result.html"
    form_template_path = "htmx/lecturer_price_card.form.html"
    webinar = get_object_or_404(Webinar, id=webinar_pk)
    service = CrmWebinarService(webinar)

    def get_result():
        lecturer_price_netto = f"{service.lecturer_price_netto():,}"
        expected_income = service.get_expected_income()
        expected_income_sign = "+" if expected_income >= 0 else "-"
        expected_income_display = (
            f"{expected_income_sign} {abs(expected_income):,}"
        )
        percent_goal = service.get_percent_goal()
        return HttpResponse(
            render_to_string(
                result_template_path,
                {
                    "webinar": webinar,
                    "lecturer_price_netto": lecturer_price_netto,
                    "percent_goal": percent_goal,
                    "percent_goal_progressbar": min(percent_goal, 100),
                    "expected_income": f"{expected_income:,}",
                    "expected_income_display": expected_income_display,
                },
            )
        )

    if mode == "result":
        return get_result()

    webinar_metadata, _ = WebinarMetadata.objects.get_or_create(webinar=webinar)

    if request.method == POST:
        form = CrmLecturerPriceCardForm(request.POST, instance=webinar_metadata)
        if form.is_valid():
            form.save()
            return get_result()
    else:
        form = CrmLecturerPriceCardForm(instance=webinar_metadata)

    return TemplateResponse(
        request,
        form_template_path,
        {
            "webinar": webinar,
            "form": form,
        },
    )
