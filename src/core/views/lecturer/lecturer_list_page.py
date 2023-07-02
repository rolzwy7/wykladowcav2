from django.template.response import TemplateResponse

from core.models import Lecturer


def lecturer_list_page(request):
    """List of lecturers"""
    template_name = "core/pages/lecturer/LecturerListPage.html"
    return TemplateResponse(
        request,
        template_name,
        {"lecturers": Lecturer.manager.visible_on_page()},
    )
