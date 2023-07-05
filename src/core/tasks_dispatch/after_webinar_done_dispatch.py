# flake8: noqa:E501
# pylint: disable=line-too-long
from celery import chain, group

from core.models import Webinar, WebinarApplication, WebinarParticipant
from core.tasks import (
    params_create_eventlog,
    params_send_participant_certificate_email,
    params_send_participant_opinion_email,
    task_create_application_invoice,
    task_create_eventlog,
    task_create_participant_certificate,
    task_save_application_invoice_metadata,
    task_send_participant_certificate_email,
    task_send_participant_opinion_email,
)


def after_webinar_done_dispatch(webinar: Webinar):
    """Performs actions after webinar is done"""

    # Prepare data
    participants = (
        WebinarParticipant.manager.get_participants_from_sent_applications(
            webinar
        )
    )
    applications = WebinarApplication.manager.sent_applications(webinar)

    invoice_jobs = [
        chain(
            task_create_application_invoice.si(application.id),  # type: ignore
            task_save_application_invoice_metadata.s(application.id),  # type: ignore
        )
        for application in applications
    ]

    certificate_jobs = [
        chain(
            task_create_participant_certificate.si(participant.id),  # type: ignore
            # Passes certificate URL to next task
            task_send_participant_certificate_email.s(
                # certificate_url passed here,
                params_send_participant_certificate_email(
                    participant.email,
                    participant.application.webinar,
                )
            ),
            # Save Weblog
            # task_create_eventlog.si(
            #     params_create_eventlog(
            #         webinar=participant.application.webinar,
            #         title_html=f"Stworzono i wysłano certyfikat ({participant.fullname})",
            #         content_html=f"E-mail: {participant.email}",
            #         icon="",
            #         color="",
            #     )
            # ),
        )
        for participant in participants
    ]

    opinion_jobs = [
        task_send_participant_opinion_email.si(
            params_send_participant_opinion_email(participant.email, webinar)
        )
        for participant in participants
    ]

    chain(
        # Send invoices
        group(*invoice_jobs),
        # Create and send certificates
        group(*certificate_jobs),
        # Queue opinion emails
        group(*opinion_jobs),
    ).apply_async()
