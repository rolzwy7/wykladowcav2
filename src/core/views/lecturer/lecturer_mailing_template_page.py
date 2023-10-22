from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Lecturer, Webinar


def lecturer_mailing_template_page(request: HttpRequest, slug: str):
    """Webinar email template page"""
    template_name = (
        "mailing_templates/MailingTemplateLecturerList/VersionA.html"
    )
    lecturer = get_object_or_404(Lecturer, slug=slug)

    lecturer_id: int = lecturer.id  # type: ignore
    webinars = Webinar.manager.get_active_webinars_for_lecturer(
        lecturer_id=lecturer_id
    )

    # Create empty groups by duration
    durations = []
    for webinar in webinars:
        duration_display = webinar.get_duration_display()  # type: ignore
        durations.append(duration_display)

    durations = list(sorted(durations))

    webinars_by_duration = {}
    for duration in durations:
        webinars_by_duration[duration] = {}

    # Create empty groups by grouping_token
    for webinar in webinars:
        duration_display = webinar.get_duration_display()  # type: ignore
        webinars_by_duration[duration_display][webinar.grouping_token] = []

    # Fill groups
    for webinar in webinars:
        duration_display = webinar.get_duration_display()  # type: ignore
        webinars_by_duration[duration_display][webinar.grouping_token].append(
            webinar
        )

    def _split_list(seq: list):
        temp = seq.copy()
        packed = []
        while temp:
            pack = temp[:2]  # get first N
            temp = temp[2:]  # delete first N
            if pack:
                packed.append(pack)
        return packed

    # Create columns
    for duration, grouping_map in webinars_by_duration.items():
        for grouping_token, webinars_seq in grouping_map.items():
            webinars_by_duration[duration][grouping_token] = _split_list(
                webinars_seq
            )

    return TemplateResponse(
        request,
        template_name,
        {
            "lecturer": lecturer,
            "webinars_map": webinars_by_duration,
            "background_color": "#f1f4fa",
            "max_width": "640px",
            "td_classes": (
                "border-collapse:collapse;"
                "padding-left:20px;"
                "padding-right:20px;"
                "font-size: 16px;"
            ),
        },
    )
