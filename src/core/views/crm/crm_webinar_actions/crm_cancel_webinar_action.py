from django.http import HttpRequest
from django.urls import reverse

from core.models.enums import WebinarStatus
from core.tasks_dispatch import after_webinar_cancel_dispatch

from .crm_webinar_actions_abstracts import CrmWebinarAction


class CancelWebinarAction(CrmWebinarAction):
    """CRM cancel webinar action"""

    def get_action_name(self):
        """Get action name"""
        return "CANCEL"

    def get_page_title(self):
        """Get page title"""
        return "Odwołaj termin szkolenia"

    def get_action_url(self):
        """Get action url"""
        webinar_pk = self.kwargs["pk"]
        return reverse("core:crm_webinar_cancel", kwargs={"pk": webinar_pk})

    def get_color(self):
        """Get color"""
        return "danger"

    def get_submit_text(self):
        """Get submit text"""
        return "Odwołaj termin"

    def get_allowed_statuses(self):
        return [WebinarStatus.INIT]

    def perform_action(self, request: HttpRequest, webinar_pk: int):
        webinar = self.get_webinar(webinar_pk)
        webinar.status = WebinarStatus.CANCELED
        after_webinar_cancel_dispatch(webinar)
        webinar.save()
