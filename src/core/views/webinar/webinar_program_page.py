"""Webinar program page"""

# flake8: noqa=E501

from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.models import ConferenceEdition, Webinar
from core.services.lecturer import LecturerService
from core.services.webinar import WebinarService


def webinar_program_page(request, slug: str):
    """Webinar program controller"""
    template_name = "geeks/pages/webinar/WebinarProgramPage.html"
    webinar = get_object_or_404(Webinar, slug=slug)
    webinar_service = WebinarService(webinar)
    lecturer_service = LecturerService(webinar.lecturer)

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
        },
    )
