from typing import Any

from django.db import transaction
from django.urls import reverse
from django.views import View

from core.models import WebinarApplication
from core.models.enums import WebinarApplicationStep

from .application_buyer_page import ApplicationBuyerPage


class ApplicationRecipientPage(ApplicationBuyerPage):
    """Application recipient page"""

    def get_action_url(self, uuid: str):
        """Get action URL for form"""
        return reverse("core:application_recipient_page", kwargs={"uuid": uuid})

    def get_company(self, application: WebinarApplication):
        """Get company"""
        return application.recipient

    def get_step_type(self):
        """Get current step type"""
        return WebinarApplicationStep.RECIPIENT

    def atomic_save(
        self, form: Any, company: Any, application: WebinarApplication
    ):
        with transaction.atomic():
            company = form.save()
            application.recipient = company
            application.save()
