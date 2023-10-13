from django.template.response import TemplateResponse


def contact_page(request):
    """Contact controller"""
    template_path = "geeks/pages/ContactPage.html"
    return TemplateResponse(request, template_path, {})
