from typing import Any

from django.db import transaction
from django.urls import reverse
from django.views import View

from core.models import WebinarApplication
from core.models.enums import WebinarApplicationStep

from .application_buyer_page import ApplicationBuyerPage


class ApplicationReceiverPage(ApplicationBuyerPage):
    """Application receiver page"""

    def get_action_url(self, uuid: str):
        """Get action URL for form"""
        return reverse("core:application_receiver_page", kwargs={"uuid": uuid})

    def get_company(self, application: WebinarApplication):
        """Get company"""
        return application.receiver

    def get_step_type(self):
        """Get current step type"""
        return WebinarApplicationStep.RECEIVER

    def atomic_save(
        self, form: Any, company: Any, application: WebinarApplication
    ):
        with transaction.atomic():
            company = form.save()
            application.receiver = company
            application.save()
