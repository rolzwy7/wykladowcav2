from django.forms import CharField, Form
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import TelegramChats
from core.consts.requests_consts import POST
from core.forms.widgets import CheckboxWidget
from core.models import Webinar
from core.models.enums import WebinarStatus
from core.tasks_dispatch import (
    dispatch_certificates_for_webinar,
    dispatch_invoices_for_webinar,
    dispatch_recording_download_for_webinar,
    dispatch_telegram_message,
)


def get_meta_redirect_url(path: str):
    """Get meta redirect url"""
    return f"{reverse('meta_redirect_page')}?path={path}"


class CrmWebinarDoneActionForm(Form):
    """Form for confirming operations"""

    send_invoices = CharField(
        widget=CheckboxWidget(
            attrs={"label": "Wyślij faktury na adresy e-mail", "checked": True}
        )
    )

    i_am_sure = CharField(
        widget=CheckboxWidget(attrs={"label": "Chcę zakończyć szkolenie"})
    )


def crm_webinar_done_action_page(request: HttpRequest, pk: int):
    """CRM done webinar action"""
    webinar = get_object_or_404(Webinar, pk=pk)
    webinar_id: int = webinar.id  # type: ignore

    if webinar.status != WebinarStatus.CONFIRMED:
        return HttpResponse(
            "Ta akcja może być wykonana tylko gdy szkolenie jest potwierdzone"
        )

    if request.method == POST:
        form = CrmWebinarDoneActionForm(request.POST)
        if form.is_valid():
            i_am_sure = form.cleaned_data["i_am_sure"] == "True"
            if not i_am_sure:
                return HttpResponse("`i_am_sure` must be `True`")

            do_send_invoices = form.cleaned_data["send_invoices"] == "True"

            Webinar.manager.filter(pk=pk).update(status=WebinarStatus.DONE)
            dispatch_certificates_for_webinar(webinar)
            if do_send_invoices:
                dispatch_invoices_for_webinar(webinar, send_via_email=True)
            else:
                dispatch_invoices_for_webinar(webinar, send_via_email=False)
            dispatch_recording_download_for_webinar(webinar)
            dispatch_telegram_message(
                f"Zrealizowano szkolenie #{webinar_id}: {webinar.title}",
                TelegramChats.OTHER,
            )
            return redirect(
                get_meta_redirect_url(
                    reverse(
                        "core:crm_webinar_detail_dashboard",
                        kwargs={"pk": webinar.pk},
                    )
                )
            )
    else:
        form = CrmWebinarDoneActionForm()

    return TemplateResponse(
        request,
        "core/pages/crm/webinar_actions/CrmWebinarDoneAction.html",
        {"form": form, "webinar": webinar},
    )
