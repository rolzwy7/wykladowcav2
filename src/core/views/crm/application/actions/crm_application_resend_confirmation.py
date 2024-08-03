"""
crm_application_resend_confirmation
"""

# flake8: noqa=E501
# pylint: disable=line-too-long
from celery import chain, group
from django.forms import CharField, Form
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.defaultfilters import date as _date
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import TelegramChats
from core.consts.requests_consts import POST
from core.forms.widgets import CheckboxWidget
from core.models import (
    Webinar,
    WebinarApplication,
    WebinarApplicationSubmitter,
    WebinarParticipant,
)
from core.tasks import (
    params_send_participant_confirmation_email,
    params_send_submitter_confirmation_email,
    task_send_participant_confirmation_email,
    task_send_submitter_confirmation_email,
    task_send_telegram_notification,
)


def get_meta_redirect_url(path: str):
    """Get meta redirect url"""
    return f"{reverse('meta_redirect_page')}?path={path}"


class CrmApplicationResendConfirmationActionForm(Form):
    """Form for confirming operations"""

    send_to_participants = CharField(
        widget=CheckboxWidget(
            attrs={
                "label": "Wyślij potwierdzenia także do uczestników",
                "checked": True,
            }
        )
    )

    i_am_sure = CharField(
        widget=CheckboxWidget(attrs={"label": "Chcę wykonać operację"})
    )


def crm_application_resend_confirmation(request: HttpRequest, pk: int):
    """CRM done webinar action"""

    application = get_object_or_404(WebinarApplication, pk=pk)
    webinar: Webinar = application.webinar
    webinar_id: int = webinar.id  # type: ignore
    application_id: int = application.id  # type: ignore
    submitter: WebinarApplicationSubmitter = application.submitter  # type: ignore
    participants = WebinarParticipant.manager.filter(application=application)

    if request.method == POST:
        form = CrmApplicationResendConfirmationActionForm(request.POST)
        if form.is_valid():
            i_am_sure = form.cleaned_data["i_am_sure"] == "True"
            send_to_participants = form.cleaned_data["send_to_participants"] == "True"
            if not i_am_sure:
                return HttpResponse("`i_am_sure` must be `True`")

            group_tasks = [
                task_send_submitter_confirmation_email.si(
                    params_send_submitter_confirmation_email(
                        submitter.email,
                        webinar_id,
                        application_id,
                    )
                )
            ]

            if send_to_participants:
                for participant in participants:
                    group_tasks.append(
                        task_send_participant_confirmation_email.si(
                            params_send_participant_confirmation_email(
                                participant.email,
                                webinar_id,
                                application_id,
                            )
                        )
                    )

            chain(
                group(*group_tasks),
                task_send_telegram_notification.si(
                    "PONOWNIE wysłano potiwerdzenie zgłoszenia\n"
                    f"Do uczestników: {'Tak' if send_to_participants else 'Nie'}\n"
                    f"Wykładowca: {webinar.lecturer}\n"
                    f"Data: {_date(webinar.date, 'j E Y')} "
                    f"godz. {_date(webinar.date, 'H:i')}\n"
                    f"#{webinar_id}: {webinar.title_original}",
                    TelegramChats.OTHER,
                ),
            ).apply_async()

            return redirect(
                get_meta_redirect_url(
                    reverse(
                        "core:crm_webinar_detail_dashboard",
                        kwargs={"pk": application.webinar.pk},
                    )
                )
            )
    else:
        form = CrmApplicationResendConfirmationActionForm()

    return TemplateResponse(
        request,
        "core/pages/crm/application_actions/CrmApplicationResendConfirmationAction.html",
        {"form": form, "application": application},
    )
