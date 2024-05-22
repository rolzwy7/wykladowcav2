"""CRM action abstract"""

# flake8: noqa=E501

from abc import ABC, abstractmethod

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View

from core.forms.crm import CrmAreYouSureForm
from core.models import Webinar, WebinarAsset


def get_meta_redirect_url(path: str):
    """Get meta redirect url"""
    return f"{reverse('meta_redirect_page')}?path={path}"


def get_not_allowed_code_msg(status: str, allowed_statuses: list[str]):
    """get_not_allowed_code_msg"""
    ret = "Ochrona przed wielokrotnym wykonaniem akcji włączona.\n\n"
    ret += "Nie można wykonać akcji.\n"
    ret += f"Aby wykonać akcję webinar musi być {allowed_statuses}.\n"
    ret += f"Obecny status webinaru {status}.\n"
    return ret


class CrmWebinarAction(ABC, View):
    """Base class for webinar actions pages"""

    template_name = "core/pages/crm/webinar_actions/CrmWebinarAction.html"

    def get_action_name(self):
        """Get action name"""
        return "[ACTION_NAME]"

    def get_page_title(self):
        """Get page title"""
        return "[PAGE_TITLE]"

    @abstractmethod
    def get_action_url(self):
        """Get action url"""
        raise NotImplementedError()

    def get_color(self):
        """Get color"""
        return "secondary"

    def get_submit_text(self):
        """Get submit text"""
        return "[SUBMIT_TEXT]"

    def get_context_data(self):
        """Get context data"""
        return {
            "action_name": self.get_action_name(),
            "page_title": self.get_page_title(),
            "action_url": self.get_action_url(),
            "color": self.get_color(),
            "submit_text": self.get_submit_text(),
        }

    def get_webinar(self, pk: int) -> Webinar:
        """Get webinar by `pk`"""
        return get_object_or_404(Webinar, pk=pk)

    def get_allowed_statuses(self):
        """Get allowed webinar statuses"""
        return []

    def get_form_class(self):
        """Get form class"""
        return CrmAreYouSureForm

    def get(self, request: HttpRequest, pk: int):
        """GET webinar action page"""
        webinar = self.get_webinar(pk)

        if webinar.status not in self.get_allowed_statuses():
            return HttpResponse(
                get_not_allowed_code_msg(webinar.status, self.get_allowed_statuses()),
                content_type="text/plain; charset=utf8",
            )

        form = self.get_form_class()()
        return TemplateResponse(
            request,
            self.template_name,
            {
                **self.get_context_data(),
                "form": form,
                "webinar": webinar,
                "webinar_assets": WebinarAsset.manager.get_for_webinar(
                    self.get_webinar(pk)
                ),
            },
        )

    def post(self, request: HttpRequest, pk: int):
        """POST webinar action page"""
        webinar = self.get_webinar(pk)

        if webinar.status not in self.get_allowed_statuses():
            return HttpResponse(
                get_not_allowed_code_msg(webinar.status, self.get_allowed_statuses()),
                content_type="text/plain; charset=utf8",
            )

        form = self.get_form_class()(request.POST)
        if form.is_valid():
            self.perform_action(request, pk)
            return redirect(
                get_meta_redirect_url(
                    reverse(
                        "core:crm_webinar_detail_dashboard",
                        kwargs={"pk": webinar.pk},
                    )
                )
            )

    @abstractmethod
    def perform_action(self, request: HttpRequest, webinar_pk: int):
        """Action to be performed after action form submit"""
        raise NotImplementedError()
