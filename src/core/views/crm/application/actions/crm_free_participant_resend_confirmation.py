"""
crm_application_resend_confirmation
"""

from celery import chain

# flake8: noqa=E501
# pylint: disable=line-too-long
from django.forms import CharField, Form
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.defaultfilters import date as _date
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import get_default_timezone

from core.consts import TelegramChats
from core.consts.requests_consts import POST
from core.forms.widgets import CheckboxWidget
from core.models import ConferenceEdition, ConferenceFreeParticipant, Webinar
from core.tasks import (
    params_send_free_participant_conference_email,
    task_send_free_participant_conference_email,
    task_send_telegram_notification,
)


def get_meta_redirect_url(path: str):
    """Get meta redirect url"""
    return f"{reverse('meta_redirect_page')}?path={path}"


class CrmFreeParticipantResendConfirmationActionForm(Form):
    """Form for confirming operations"""

    i_am_sure = CharField(
        widget=CheckboxWidget(attrs={"label": "Chcę wykonać operację"})
    )


def crm_free_participant_resend_confirmation(request: HttpRequest, pk: int):
    """CRM done webinar action"""

    participant = get_object_or_404(ConferenceFreeParticipant, pk=pk)
    edition: ConferenceEdition = participant.edition
    webinar: Webinar = edition.webinar
    webinar_id: int = webinar.id  # type: ignore

    if request.method == POST:
        form = CrmFreeParticipantResendConfirmationActionForm(request.POST)
        if form.is_valid():
            i_am_sure = form.cleaned_data["i_am_sure"] == "True"
            if not i_am_sure:
                return HttpResponse("`i_am_sure` must be `True`")

            # Perform action
            tz = get_default_timezone()
            webinar_date = edition.webinar.date

            chain(
                # Send e-mail with conference URL
                task_send_free_participant_conference_email.si(
                    params_send_free_participant_conference_email(
                        webinar.title,
                        participant.email,
                        reverse(
                            "core:conference_waiting_room_page",
                            kwargs={
                                "watch_token": str(participant.watch_token),
                            },
                        ),
                        _date(webinar_date.astimezone(tz), "j E Y"),
                        _date(webinar_date.astimezone(tz), "H:i"),
                    )
                ),
                # Send telegram notification
                task_send_telegram_notification.si(
                    f"PONOWNIE wysłano potwierdzenie do darmowego uczestnika"
                    f"({participant.email}) : {edition.webinar.title}",
                    TelegramChats.OTHER,
                ),
            ).apply_async()

            return redirect(
                get_meta_redirect_url(
                    reverse(
                        "core:crm_webinar_free_participants",
                        kwargs={"pk": webinar_id},
                    )
                )
            )
    else:
        form = CrmFreeParticipantResendConfirmationActionForm()

    return TemplateResponse(
        request,
        "core/pages/crm/application_actions/CrmFreeParticipantResendConfirmationAction.html",
        {"form": form, "participant": participant},
    )
