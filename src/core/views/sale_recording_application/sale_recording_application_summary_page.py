"""Application form summary"""

# flake8: noqa:E501

from celery import chain
from django.shortcuts import get_object_or_404, redirect
from django.template.defaultfilters import date as _date
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST, TelegramChats
from core.forms import SaleRecordingApplicationSummarySubmitForm
from core.models import SaleRecordingApplication, SaleRecordingParticipant, Webinar
from core.models.enums import ApplicationStatus, WebinarApplicationStep
from core.tasks import (
    params_send_sale_recording_order_email,
    task_sale_recording_create_application_invoice,
    task_send_sale_recording_order_email,
    task_send_telegram_notification,
)

APPLICATION_STEP = WebinarApplicationStep.SUMMARY


def sale_recording_application_summary_page(request, uuid):
    """Application summary page"""

    template_name = "geeks/pages/sale_recording_application/ApplicationSummaryPage.html"

    application = get_object_or_404(SaleRecordingApplication, uuid=uuid)
    application_id: int = application.id  # type: ignore
    webinar: Webinar = application.sale_recording.recording.webinar
    webinar_id: int = webinar.id  # type: ignore

    participants = (
        SaleRecordingParticipant.manager.get_all_participants_for_application(
            application=application
        )
    )

    if application.application_type == "PRIVATE_PERSON":
        order_email: str = application.private_person.email  # type: ignore
    else:
        order_email: str = application.buyer.email  # type: ignore

    if request.method == POST and application.status == ApplicationStatus.INIT:
        form = SaleRecordingApplicationSummarySubmitForm(request.POST)
        if form.is_valid():

            # Dispatch tasks
            chain(
                task_sale_recording_create_application_invoice.si(application_id),
                task_send_sale_recording_order_email.si(
                    params_send_sale_recording_order_email(order_email, application_id)
                ),
                task_send_telegram_notification.si(
                    f"Zamówienie dostępu do nagrania #{application_id} na szkolenie\n"
                    f"Wykładowca: {webinar.lecturer}\n"
                    f"z dnia: {_date(webinar.date, 'j E Y')} "
                    f"godz. {_date(webinar.date, 'H:i')}\n"
                    f"#{webinar_id}: {webinar.title_original}",
                    TelegramChats.APPLICATIONS,
                ),
            ).apply_async()

            application.save()

            return redirect(reverse("core:sale_recording_application_success_page"))
    else:
        form = SaleRecordingApplicationSummarySubmitForm()

    return TemplateResponse(
        request,
        template_name,
        {
            "step_number": 2 if application.application_type == "PRIVATE_PERSON" else 4,
            "step_title": "Podsumowanie",
            "step_description": "Podsumowanie opis",
            "application": application,
            "webinar": webinar,
            "participants": participants,
            "form": form,
            "total_price": participants.count() * application.price_netto,
        },
    )
