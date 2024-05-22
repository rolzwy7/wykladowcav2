"""CRM webinar send opiniton requests action"""

# flake8: noqa=E501

from django.http import HttpRequest
from django.urls import reverse

from core.models.enums import WebinarStatus
from core.services.webinar import WebinarService
from core.tasks_dispatch import dispatch_opinion_requests

from .crm_webinar_actions_abstracts import CrmWebinarAction


class WebinarSendOpinionRequestsAction(CrmWebinarAction):
    """WebinarSendOpinionRequestsAction"""

    def get_action_name(self):
        """Get action name"""
        return "SEND_OPINION_REQUESTS"

    def get_page_title(self):
        """Get page title"""
        return "Prześlij prośby o opinie"

    def get_action_url(self):
        """Get action url"""
        webinar_pk = self.kwargs["pk"]
        return reverse(
            "core:crm_webinar_send_opinion_request_action", kwargs={"pk": webinar_pk}
        )

    def get_color(self):
        """Get color"""
        return "info"

    def get_submit_text(self):
        """Get submit text"""
        return "Prześlij prośby o opinie"

    def get_allowed_statuses(self):
        return [WebinarStatus.DONE]

    def perform_action(self, request: HttpRequest, webinar_pk: int):
        webinar_pk = self.kwargs["pk"]
        dispatch_opinion_requests(self.get_webinar(webinar_pk))
