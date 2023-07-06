from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar
from core.services import WebinarService


def webinar_opinions_page(request, slug: str):
    template_name = "core/pages/webinar/WebinarOpinionsPage.html"
    webinar = get_object_or_404(Webinar, slug=slug)
    service = WebinarService(webinar)
    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "webinar_tabs": service.get_webinar_tabs(1),
            **service.get_context(),
        },
    )
