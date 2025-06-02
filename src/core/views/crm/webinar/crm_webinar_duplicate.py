from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import now

from core.consts import POST
from core.models import Webinar
from core.models.enums.webinar_enums import WebinarStatus
from core.services.webinar import WebinarService


def crm_webinar_duplicate(request, pk: int):
    """Duplicate webinar"""
    webinar = get_object_or_404(Webinar, pk=pk)
    webinar_service = WebinarService(webinar)
    template_name = "core/pages/crm/CrmDuplicateWebinar.html"

    if request.method == POST:
        temp_categories = [_ for _ in webinar.categories.all()]
        webinar.id = None  # type: ignore
        webinar.slug = ""
        webinar.status = WebinarStatus.INIT
        webinar.created_at = now()
        webinar.save()
        webinar_id: int = webinar.id  # type: ignore
        for cat in temp_categories:
            webinar.categories.add(cat)
        return redirect(
            reverse("admin:core_webinar_change", kwargs={"object_id": webinar_id})
        )

    return TemplateResponse(
        request,
        template_name,
        {
            "webinar": webinar,
            "related_webinars": webinar_service.get_related_webinars(),
        },
    )
