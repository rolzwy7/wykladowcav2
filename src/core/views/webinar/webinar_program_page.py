from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar
from core.utils.webinar import get_webinar_tabs


def webinar_program_page(request, slug: str):
    template_name = "core/pages/webinar/WebinarProgramPage.html"
    webinar = get_object_or_404(Webinar, slug=slug)
    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "webinar_tabs": get_webinar_tabs(0, webinar.slug),
        },
    )
