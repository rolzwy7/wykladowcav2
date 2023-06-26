from django.template.response import TemplateResponse


def application_exception_handler_page(request):
    template_name = "core/pages/application/ApplicationTooLate.html"
    context = {}
    return TemplateResponse(request, template_name, context)
