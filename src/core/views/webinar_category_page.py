from django.template.response import TemplateResponse


def webinar_category_page(request, slug: str):
    template_name = "core/pages/WebinarCategoryPage.html"
    return TemplateResponse(
        request,
        template_name,
        {},
    )
