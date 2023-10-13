from django.template.response import TemplateResponse

from core.models.lecturer_model import Lecturer


def lecturer_list_page(request):
    """Lecturer list page"""
    template_name = "core/pages/crm/lecturer/LecturerListPage.html"
    lecturers = Lecturer.manager.all()
    return TemplateResponse(request, template_name, {"lecturers": lecturers})
