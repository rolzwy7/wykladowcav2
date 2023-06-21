from django.template.response import TemplateResponse


def lecturer_list_page(request):
    template_name = "core/pages/LecturerListPage.html"
    return TemplateResponse(
        request,
        template_name,
        {},
    )
