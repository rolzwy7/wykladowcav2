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

    webinars_seq = [webinar for webinar in webinars]
    webinars_packed: list[list[Webinar]] = []
    while webinars_seq:
        webinar_pack = webinars_seq[:3]  # get first N
        webinars_seq = webinars_seq[3:]  # delete first N
        if webinar_pack:
            webinars_packed.append(webinar_pack)

    return TemplateResponse(
        request,
        template_name,
        {
            "lecturer": lecturer,
            "webinars_packed": webinars_packed,
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
