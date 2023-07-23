# flake8: noqa:E501
# pylint: disable=line-too-long

from django.utils.timezone import datetime

from core.models import (
    Webinar,
    WebinarApplication,
    WebinarApplicationSubmitter,
    WebinarMoveRegister,
    WebinarMoveRegisterItem,
)
from core.tasks import (
    params_send_submitter_moving_email,
    task_send_submitter_moving_email,
)


def after_webinar_moved_dispatch(webinar: Webinar, new_date: datetime):
    """Performs actions after webinar is moved"""

    # Get sent applications for this webinar
    sent_applications = WebinarApplication.manager.sent_applications(webinar)

    # Create move register object
    move_register = WebinarMoveRegister(
        webinar=webinar,
        from_datetime=webinar.date,
        to_datetime=new_date,
        applications_count=sent_applications.count(),
    )
    move_register.save()
    move_register_id: int = move_register.id  # type: ignore

    # Save new date for webinar
    webinar.date = new_date
    webinar.save()

    # Create move register items
    for sent_application in sent_applications:
        application_id: int = sent_application.id  # type: ignore
        submitter: WebinarApplicationSubmitter = sent_application.submitter  # type: ignore

        register_item = WebinarMoveRegisterItem(
            move_register=move_register,
            application=sent_application,
        )
        register_item.save()

        # Dispatch sending moving e-mail task
        task_send_submitter_moving_email.si(
            params_send_submitter_moving_email(
                submitter.email,
                application_id,
                move_register_id,
                str(register_item.token),
            )
        ).apply_async()
