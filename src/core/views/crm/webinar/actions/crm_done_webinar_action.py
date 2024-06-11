"""CRM done action"""

# flake8: noqa=E501
# pylint: disable=line-too-long

from django.forms import CharField, Form
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import TelegramChats
from core.consts.requests_consts import POST
from core.forms.widgets import CheckboxWidget
from core.models import Lecturer, Webinar
from core.models.enums import WebinarStatus
from core.tasks.create_crm_todo.procedure import create_crm_todo
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

    i_am_sure = CharField(
        widget=CheckboxWidget(attrs={"label": "Chcę zakończyć szkolenie"})
    )

    send_invoices_via_email = CharField(
        widget=CheckboxWidget(
            attrs={
                "label": "Wyślij faktury poprzez e-mail (jeśli zostały stworzone)",
                "checked": True,
            }
        )
    )

    fakturownia_create_invoices = CharField(
        widget=CheckboxWidget(
            attrs={
                "label": "Stwórz faktury w Fakturowni",
                "checked": True,
            }
        )
    )

    send_certificates = CharField(
        widget=CheckboxWidget(
            attrs={
                "label": "Stwórz i wyślij certyfikaty na adresy e-mail uczestników",
                "checked": True,
            }
        )
    )

    start_recording_download_procedure = CharField(
        widget=CheckboxWidget(
            attrs={
                "label": "Rozpocznij pobieranie nagrania w celu udostępnienia uczesnitkom",
                "checked": True,
            }
        )
    )


def crm_webinar_done_action_page(request: HttpRequest, pk: int):
    """CRM done webinar action"""
    webinar = get_object_or_404(Webinar, pk=pk)
    webinar_id: int = webinar.id  # type: ignore
    lecturer: Lecturer = webinar.lecturer

    if webinar.status != WebinarStatus.CONFIRMED:
        return HttpResponse(
            "Ta akcja może być wykonana tylko gdy szkolenie jest potwierdzone"
        )

    if request.method == POST:
        form = CrmWebinarDoneActionForm(request.POST)
        if form.is_valid():

            # Flags
            flag_i_am_sure = form.cleaned_data["i_am_sure"] == "True"
            flag_fakturownia_create_invoices = (
                form.cleaned_data["fakturownia_create_invoices"] == "True"
            )
            flag_send_certificates = form.cleaned_data["send_certificates"] == "True"
            flag_start_recording_download_procedure = (
                form.cleaned_data["start_recording_download_procedure"] == "True"
            )
            flag_send_invoices_via_email = (
                form.cleaned_data["send_invoices_via_email"] == "True"
            )

            # Check if user admited he knew what he is doing
            if not flag_i_am_sure:
                return HttpResponse("`i_am_sure` must be `True`")

            # Mark this webinar as done
            Webinar.manager.filter(pk=pk).update(status=WebinarStatus.DONE)

            # Create task for opinion requests
            if lecturer.agrees_to_recording:
                create_crm_todo(
                    f"Opinie o wykładowcy - {lecturer.fullname}",
                    f"Wyślij prośby o opinie do wykładowcy do uczestników szkolenia {webinar.title}",
                    "sms",
                    "success",
                    reverse(
                        "core:crm_webinar_send_opinion_request_action",
                        kwargs={"pk": webinar_id},
                    ),
                    webinar_id=webinar_id,
                )

            # Send invoices via email (if selected)
            if flag_fakturownia_create_invoices:
                dispatch_invoices_for_webinar(
                    webinar,
                    send_via_email=flag_send_invoices_via_email,
                )

            # Dispatch certificates (if selected)
            if flag_send_certificates:
                dispatch_certificates_for_webinar(webinar)

            # Start downloading webinar recording (if selected)
            if flag_start_recording_download_procedure:
                dispatch_recording_download_for_webinar(webinar)
                create_crm_todo(
                    f"Dostępy do nagrań - {lecturer.fullname}",
                    f"Wyślij dostępy do nagrań dla uczestników szkolenia <i>{webinar.title}</i>",
                    "youtube",
                    "success",
                    reverse(
                        "core:crm_webinar_recordings",
                        kwargs={"pk": webinar_id},
                    ),
                    webinar_id=webinar_id,
                )

            dispatch_telegram_message(
                f"Zrealizowano szkolenie #{webinar_id}\n"
                f"Tytuł: {webinar.title}\n"
                f"Wykładowca: {lecturer.fullname}\n\n"
                f"Stwórz faktury: {'Tak' if flag_fakturownia_create_invoices else 'Nie'}"
                f"Wyślij faktury przez e-mail: {'Tak' if flag_send_invoices_via_email else 'Nie'}"
                f"Certyfikaty: {'Tak' if flag_send_certificates else 'Nie'}"
                f"Rozpocznij pobieranie: {'Tak' if flag_start_recording_download_procedure else 'Nie'}",
                TelegramChats.OTHER,
            )

            # Redirect to CRM dashboard
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
