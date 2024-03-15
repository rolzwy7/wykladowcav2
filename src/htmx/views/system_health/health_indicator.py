"""Health indicator"""

from django.template.response import TemplateResponse

from core.services import HealthcheckService


def health_indicator(request):
    """Health indicator"""
    template_name = "htmx/system_health/health_indicator.html"

    healtcheck_service = HealthcheckService()

    return TemplateResponse(
        request,
        template_name,
        {"color": "success" if healtcheck_service.is_healthy() else "danger"},
    )
