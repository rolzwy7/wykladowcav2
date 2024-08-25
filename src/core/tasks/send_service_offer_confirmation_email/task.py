"""Task"""

# flake8: noqa=E501

import json

from core.tasks.base_task import BaseTaskWithRetry
from wykladowcapl.celery import app

from .procedure import (
    SendServiceOfferConfirmationEmailParams,
    send_service_offer_confirmation_email,
)


@app.task(name="send_service_offer_confirmation_email", base=BaseTaskWithRetry)
def task_send_service_offer_confirmation_email(serialized_params: str):
    """Task for `send_service_offer_confirmation_email`"""
    send_service_offer_confirmation_email(
        SendServiceOfferConfirmationEmailParams(**json.loads(serialized_params))
    )
