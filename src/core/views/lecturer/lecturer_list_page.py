from django.http import HttpResponsePermanentRedirect
from django.template.response import TemplateResponse

from core.models import Lecturer, WebinarCategory


def lecturer_list_page(request):
    """List of lecturers"""

    return HttpResponsePermanentRedirect("/")

    template_name = "geeks/pages/lecturers/LecturerListPage.html"

    main_categories = WebinarCategory.manager.get_main_categories()
    lecturers = Lecturer.manager.get_lecturers_visible_on_page()

    category_lecturers_map = {category: [] for category in main_categories}

    for category in main_categories:
        for lecturer in lecturers:
            if category in lecturer.categories.all():
                category_lecturers_map[category].append(lecturer)

    return TemplateResponse(
        request,
        template_name,
        {"category_lecturers_map": category_lecturers_map},
    )
