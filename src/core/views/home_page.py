from django.template.response import TemplateResponse

from core.models import Lecturer, Webinar


def home_page(request):
    """Homepage controller"""
    template_name = "core/pages/HomePage3.html"
    context = {
        "webinars": Webinar.manager.homepage_webinars(),
        "visible_lecturers": Lecturer.manager.visible_on_page(),
    }
    return TemplateResponse(request, template_name, context)
