from django.template.response import TemplateResponse

from core.models import Webinar


def contact_page(request):
    """Contact controller"""
    template_path = "core/pages/ContactPage.html"
    context = {"webinars": Webinar.manager.homepage_webinars()}
    return TemplateResponse(request, template_path, context)
