from django.template.response import TemplateResponse


def sale_recording_application_exception_handler_page(request):  # TODO: ???
    template_name = "core/pages/application/ApplicationTooLate.html"
    context = {}
    return TemplateResponse(request, template_name, context)
