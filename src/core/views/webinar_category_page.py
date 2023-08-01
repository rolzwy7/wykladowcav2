from django.template.response import TemplateResponse

from core.models import Webinar


def webinar_category_page(request, slug: str):
    """Webinar category page"""
    template_name = "core/pages/WebinarCategoryPage.html"

    if slug == "wszystkie":
        webinars = Webinar.manager.homepage_webinars()
    else:
        webinars = Webinar.manager.webinars_for_category(slug)

    return TemplateResponse(
        request,
        template_name,
        {"webinars": webinars},
    )
