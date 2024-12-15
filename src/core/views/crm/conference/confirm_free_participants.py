"""conference_from_webinar"""

# flake8: noqa=E501
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts.requests_consts import POST
from core.forms.crm import CrmAreYouSureForm
from core.models.conference import ConferenceEdition
from core.models.webinar_model import Webinar
from core.tasks_dispatch import after_conference_confirm_dispatch


def confirm_free_participants(request, pk: int):
    """confirm_free_participants"""
    template_name = "core/pages/crm/CrmConferenceConfirmFreeParticipants.html"

    edition = get_object_or_404(ConferenceEdition, pk=pk)
    webinar: Webinar = edition.webinar

    error = ""

    if request.method == POST:
        form = CrmAreYouSureForm(request.POST)
        if form.is_valid():

            if form.cleaned_data["i_am_sure"] == "True":
                after_conference_confirm_dispatch(edition)
                # Redirect to CRM dashboard
                return redirect(
                    reverse(
                        "core:crm_webinar_detail_dashboard", kwargs={"pk": webinar.pk}
                    )
                )
            else:
                error = "Zaznacz checkbox, że jesteś pewien"
    else:
        form = CrmAreYouSureForm()

    return TemplateResponse(
        request,
        template_name,
        {"edition": edition, "webinar": webinar, "form": form, "error": error},
    )
