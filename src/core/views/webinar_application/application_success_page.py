from django.template.response import TemplateResponse


def application_success_page(request):
    """Application success page"""
    template_name = "core/pages/application/ApplicationSuccessPage.html"
    context = {}
    return TemplateResponse(request, template_name, context)
