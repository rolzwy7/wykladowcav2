from django.template.response import TemplateResponse

from core.models import Webinar


def home_page(request):
    context = {"webinars": Webinar.manager.homepage_webinars()}
    return TemplateResponse(request, "core/pages/Homepage.html", context)
