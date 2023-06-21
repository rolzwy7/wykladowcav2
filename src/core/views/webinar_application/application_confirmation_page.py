from django.template.response import TemplateResponse


def application_confirmation_page(request):
    template_name = "core/pages/application_confirmation_page.html"
    context = {}
    return TemplateResponse(request, template_name, context)
