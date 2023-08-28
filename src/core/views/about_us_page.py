from django.template.response import TemplateResponse


def about_us_page(request):
    """About us controller"""
    template_path = "geeks/pages/AboutUsPage.html"
    return TemplateResponse(request, template_path, {})
