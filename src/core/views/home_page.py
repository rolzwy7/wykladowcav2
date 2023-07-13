from django.template.response import TemplateResponse

from core.models import Webinar


def home_page(request):
    """Homepage controller"""
    template_name = "core/pages/HomePage.html"
    context = {"webinars": Webinar.manager.homepage_webinars()}
    return TemplateResponse(request, template_name, context)
