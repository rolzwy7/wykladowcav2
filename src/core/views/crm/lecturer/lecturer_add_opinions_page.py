from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts import POST
from core.forms.crm import CrmLecturerAddOpinionsForm
from core.models import Lecturer, LecturerOpinion


def lecturer_add_opinions_page(request, pk: int):
    """Lecturer add opinions page"""
    template_name = "core/pages/crm/lecturer/LecturerAddOpinionsPage.html"
    lecturer = get_object_or_404(Lecturer, pk=pk)

    if request.method == POST:
        form = CrmLecturerAddOpinionsForm(request.POST)
        if form.is_valid():
            opinions = request.POST["opinions"]
            for opinion in opinions.split("\r\n"):
                opinion_normalized = opinion.strip()
                if not opinion_normalized:
                    continue
                a = 1  # TODO
    else:
        form = CrmLecturerAddOpinionsForm()

    return TemplateResponse(request, template_name, {"lecturer": lecturer})
