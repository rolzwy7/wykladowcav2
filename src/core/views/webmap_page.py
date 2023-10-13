from django.template.response import TemplateResponse


def webmap_page(request):
    """Webmap controller"""
    template_path = "geeks/pages/WebmapPage.html"
    return TemplateResponse(request, template_path, {})
