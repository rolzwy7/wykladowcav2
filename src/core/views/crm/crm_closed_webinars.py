from django.template.response import TemplateResponse

from core.models import ClosedWebinarContactMessage


def crm_closed_webinars(request):
    """crm_closed_webinars"""
    template_name = "core/pages/crm/CrmClosedWebinars.html"
    return TemplateResponse(
        request,
        template_name,
        {
            "contact_messages": ClosedWebinarContactMessage.objects.all().order_by(
                "-created_at"
            )
        },
    )
