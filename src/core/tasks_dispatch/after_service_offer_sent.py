"""
Procedure that executes after webinar application has been sent
"""

# flake8: noqa=E501

from celery import chain

from core.consts import TelegramChats
from core.models import ServiceOffer, ServiceOfferApplication
from core.tasks import task_send_telegram_notification
from core.tasks.send_service_offer_confirmation_email import (
    params_send_service_offer_confirmation_email,
    task_send_service_offer_confirmation_email,
)


def after_service_offer_sent(
    service_offer: ServiceOffer, application: ServiceOfferApplication
):
    """Dispatch tasks after application sent"""

    # Dispatch tasks
    chain(
        task_send_service_offer_confirmation_email.si(
            params_send_service_offer_confirmation_email(
                application.email_contact, service_offer.offer_title
            )
        ),
        task_send_telegram_notification.si(
            f"Wysłano zapytanie ofertowe: {application.email_contact} {service_offer.offer_title}",
            TelegramChats.OTHER,
        ),
    ).apply_async()
