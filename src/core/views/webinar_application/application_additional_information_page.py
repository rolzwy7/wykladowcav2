from django.template.response import TemplateResponse


def application_additional_information_page(request):
    template_name = "core/pages/application/AdditionalInformationPage.html"
    context = {}
    return TemplateResponse(request, template_name, context)
