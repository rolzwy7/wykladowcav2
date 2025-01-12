"""Webinar program page"""

# flake8: noqa=E501

from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.models import ConferenceEdition, Webinar
from core.services import OpinionsService
from core.services.lecturer import LecturerService
from core.services.webinar import WebinarService


def webinar_termin_page_v3(request, slug: str):
    """webinar_termin_page_v3"""
    template_name = "geeks/pages/webinarv3/WebinarTerminPage.html"

    webinar = get_object_or_404(Webinar, slug=slug)

    if webinar.is_connected_to_conference:
        try:
            edition: ConferenceEdition = ConferenceEdition.manager.get(webinar=webinar)
        except ConferenceEdition.DoesNotExist:  # pylint: disable=no-member
            return redirect("/")
        else:
            return redirect(
                reverse(
                    "core:conference_edition_page",
                    kwargs={"slug_edition": edition.slug},
                )
            )

    webinar_service = WebinarService(webinar)
    lecturer_service = LecturerService(webinar.lecturer)
    opinions_service = OpinionsService(lecturer_service.get_lecturer_opinions())

    return TemplateResponse(
        request,
        template_name,
        {
            "META__TITLE": webinar.title,
            "CANONICAL": reverse(
                "core:webinar_program_page", kwargs={"slug": webinar.slug}
            ),
            "webinar": webinar,
            "related_webinars": webinar_service.get_related_webinars(),
            "similar_webinars": webinar_service.get_similar_webinars(),
            "webinar_tabs": webinar_service.get_webinar_tabs(0),
            "lecturer_service": lecturer_service,
            "opinions_page": opinions_service.get_opinions_page(1, per_page=15),
            "opinions_average": opinions_service.get_opinions_average(),
            "opinions_breakdown": opinions_service.get_opinions_breakdown(),
        },
    )
