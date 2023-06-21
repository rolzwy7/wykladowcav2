from django.template.response import TemplateResponse


def register_page(request):
    template_name = "core/pages/RegisterPage.html"
    return TemplateResponse(
        request,
        template_name,
        {},
    )
