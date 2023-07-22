from django.http import HttpRequest
from django.urls import reverse

from core.models.enums import WebinarStatus
from core.tasks_dispatch import after_webinar_done_dispatch

from .crm_webinar_actions_abstracts import CrmWebinarAction


class DoneWebinarAction(CrmWebinarAction):
    """CRM done webinar action"""

    def get_action_name(self):
        """Get action name"""
        return "DONE"

    def get_page_title(self):
        """Get page title"""
        return "Zakończ szkolenia"

    def get_action_url(self):
        """Get action url"""
        webinar_pk = self.kwargs["pk"]
        return reverse("core:crm_webinar_done", kwargs={"pk": webinar_pk})

    def get_color(self):
        """Get color"""
        return "success"

    def get_submit_text(self):
        """Get submit text"""
        return "Zakończ szkolenie"

    def get_allowed_statuses(self):
        return [WebinarStatus.CONFIRMED]

    def perform_action(self, request: HttpRequest, webinar_pk: int):
        webinar = self.get_webinar(webinar_pk)
        webinar.status = WebinarStatus.DONE
        after_webinar_done_dispatch(webinar)
        webinar.save()
