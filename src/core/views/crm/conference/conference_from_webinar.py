"""conference_from_webinar"""

# flake8: noqa=E501
from django.db import transaction
from django.forms import ModelForm, Select, TextInput
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts.requests_consts import POST
from core.libs.clickmeeting import create_free_clickmeeting_room
from core.models.conference import ConferenceEdition
from core.models.enums import WEBINAR_CLICKMEETING_DURATION
from core.models.webinar_model import Webinar


class ConferenceEditionModelForm(ModelForm):
    """ConferenceEditionModelForm"""

    class Meta:
        """meta"""

        model = ConferenceEdition
        fields = [
            "cycle",
            "stream_type",
            # "stream_url_page",
            "stream_server_url",
            "stream_transmission_key",
            "slug",
            "webinar",
        ]
        widgets = {
            "cycle": Select(attrs={"class": "form-control"}),
            "stream_type": Select(attrs={"class": "form-control"}),
            # "stream_url_page": TextInput(attrs={"class": "form-control"}),
            "stream_server_url": TextInput(attrs={"class": "form-control"}),
            "stream_transmission_key": TextInput(attrs={"class": "form-control"}),
            "slug": TextInput(attrs={"class": "form-control"}),
            "webinar": Select(attrs={"class": "form-control"}),
        }


def conference_from_webinar(request, pk: int):
    """conference_from_webinar"""
    template_name = "core/pages/crm/CrmConferenceFromWebinar.html"

    webinar = get_object_or_404(Webinar, pk=pk)

    if webinar.is_connected_to_conference:
        return HttpResponse("Ten webinar jest już połączony z konferencją")

    if request.method == POST:
        form = ConferenceEditionModelForm(request.POST)
        if form.is_valid():

            with transaction.atomic():
                # Mark as
                webinar.is_connected_to_conference = True
                webinar.remaining_places = 0
                webinar.save()
                edition: ConferenceEdition = form.save()

            # Create room in clickmeeting
            try:
                room_id, clickmeeting_url = create_free_clickmeeting_room(
                    room_name=webinar.title,
                    lobby_description=webinar.program,
                    date=webinar.date,
                    duration=WEBINAR_CLICKMEETING_DURATION[webinar.duration],
                )
                edition.clickmeeting_id = str(room_id)
                edition.clickmeeting_url = clickmeeting_url
                edition.save()
            except Exception as e:  # pylint: disable=broad-exception-caught
                return HttpResponse(
                    f"Coś się zepsuło przy tworzeniu pokoju. Prześlij mi to:\n `{e}`",
                    content_type="text/plain; charset=utf8",
                )

            # Redirect to CRM dashboard
            return redirect(
                reverse("core:crm_webinar_detail_dashboard", kwargs={"pk": webinar.pk})
            )
    else:
        form = ConferenceEditionModelForm(
            initial={"webinar": webinar, "slug": f"bezplatny-webinar-{webinar.slug}"}
        )

    return TemplateResponse(
        request,
        template_name,
        {"webinar": webinar, "form": form},
    )
