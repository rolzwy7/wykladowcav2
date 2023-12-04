# flake8: noqa=E501
# pylint: disable=line-too-long
from django.forms import CharField, Form
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts.requests_consts import POST
from core.forms.widgets import CheckboxWidget
from core.models import WebinarApplication
from core.tasks_dispatch import dispatch_invoice_for_application


def get_meta_redirect_url(path: str):
    """Get meta redirect url"""
    return f"{reverse('meta_redirect_page')}?path={path}"


class CrmApplicationSendInvoiceActionForm(Form):
    """Form for confirming operations"""

    send_invoice = CharField(
        widget=CheckboxWidget(
            attrs={"label": "Wyślij fakturę na adres e-mail", "checked": True}
        )
    )

    i_am_sure = CharField(
        widget=CheckboxWidget(attrs={"label": "Chcę przesłać fakturę"})
    )


def crm_application_send_invoice_action_page(request: HttpRequest, pk: int):
    """CRM done webinar action"""
    application = get_object_or_404(WebinarApplication, pk=pk)

    if request.method == POST:
        form = CrmApplicationSendInvoiceActionForm(request.POST)
        if form.is_valid():
            send_invoice = form.cleaned_data["send_invoice"] == "True"
            i_am_sure = form.cleaned_data["i_am_sure"] == "True"
            if not i_am_sure:
                return HttpResponse("`i_am_sure` must be `True`")

            dispatch_invoice_for_application(application, send_via_email=send_invoice)

            return redirect(
                get_meta_redirect_url(
                    reverse(
                        "core:crm_webinar_detail_dashboard",
                        kwargs={"pk": application.webinar.pk},
                    )
                )
            )
    else:
        form = CrmApplicationSendInvoiceActionForm()

    return TemplateResponse(
        request,
        "core/pages/crm/application_actions/CrmApplicationSendInvoiceAction.html",
        {"form": form, "application": application},
    )
