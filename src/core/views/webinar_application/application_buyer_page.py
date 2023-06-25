from typing import Any

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View

from core.forms import ApplicationCompanyForm
from core.models import WebinarApplication
from core.models.enums import WebinarApplicationStep
from core.structs import ApplicationStepState


class ApplicationBuyerPage(View):
    """Abstract base class for company application steps

    Use this abstract class to construct views for `buyer` and `receiver`
    """

    template_name = "core/pages/application/ApplicationCompanyPage.html"

    def get_action_url(self, uuid: str):
        """Get action URL for form"""
        return reverse("core:application_buyer_page", kwargs={"uuid": uuid})

    def get_company(self, application: WebinarApplication):
        """Get company"""
        return application.buyer

    def get_step_type(self):
        """Get current step type"""
        return WebinarApplicationStep.BUYER

    def get_form_class(self):
        """Get current step type"""
        return ApplicationCompanyForm

    def atomic_save(
        self, form: Any, company: Any, application: WebinarApplication
    ):
        with transaction.atomic():
            company = form.save()
            application.buyer = company
            application.save()

    def _get_application(self, uuid: str):
        """Get application"""
        return get_object_or_404(WebinarApplication, uuid=uuid)

    def _get_template_response(self, request, uuid, form, state):
        return TemplateResponse(
            request,
            self.template_name,
            {
                "form": form,
                "action_url": self.get_action_url(uuid),
                **state.get_context(),
            },
        )

    def get(self, request, uuid: str):
        """Handle GET request"""
        application = self._get_application(uuid)
        webinar = application.webinar
        company = self.get_company(application)
        form_class = self.get_form_class()
        form = form_class(instance=company)
        state = ApplicationStepState(webinar, application, self.get_step_type())
        return self._get_template_response(request, uuid, form, state)

    def post(self, request, uuid: str):
        """Handle POST request"""
        application = self._get_application(uuid)
        webinar = application.webinar
        company = self.get_company(application)
        form_class = self.get_form_class()
        state = ApplicationStepState(webinar, application, self.get_step_type())

        form = form_class(request.POST, instance=company)
        if form.is_valid():
            self.atomic_save(form, company, application)
            return state.get_next_step_redirect()

        return self._get_template_response(request, uuid, form, state)


# def application_buyer_page(request, uuid: str):
#     """Controller for `buyer` application step"""
#     template_name = "core/pages/application/ApplicationBuyerPage.html"
#     application = get_object_or_404(WebinarApplication, uuid=uuid)
#     webinar = application.webinar
#     buyer = application.buyer  # None or WebinarApplicationCompany
#     state = ApplicationStepState(
#         webinar, application, WebinarApplicationStep.BUYER
#     )

#     if request.method == POST:
#         form = ApplicationCompanyForm(request.POST, instance=buyer)
#         if form.is_valid():
#             with transaction.atomic():
#                 buyer = form.save()
#                 application.buyer = buyer
#                 application.save()
#             return state.get_next_step_redirect()
#     else:
#         form = ApplicationCompanyForm(instance=buyer)

#     return TemplateResponse(
#         request,
#         template_name,
#         {"form": form, **state.get_context()},
#     )
