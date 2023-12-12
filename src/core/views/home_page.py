from django.template.response import TemplateResponse

from core.services import HomepageService


def home_page(request):
    """Homepage controller"""
    template_name = "geeks/pages/homepage/HomePage.html"
    homepage_service = HomepageService()
    return TemplateResponse(
        request,
        template_name,
        homepage_service.get_context(),
    )
