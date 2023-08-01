from django.template.response import TemplateResponse

from core.models import Webinar


def contact_page(request):
    """Contact controller"""
    template_path = "core/pages/ContactPage.html"
    return TemplateResponse(request, template_path, {})
