from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import LecturerOpinionForm
from core.models import Lecturer, LecturerOpinion
from core.services.lecturer import LecturerService
from core.tasks.create_crm_todo.procedure import create_crm_todo


def lecturer_opinion_form_page(request, slug: str):
    """Lecturer opinion form page"""
    template_name = "geeks/pages/lecturer/LecturerOpinionFormPage.html"
    lecturer = get_object_or_404(Lecturer, slug=slug)
    if lecturer.finished_coop:
        raise Http404("Zakończono współpracę")

    service = LecturerService(lecturer)

    if request.method == POST:
        form = LecturerOpinionForm(request.POST)
        if form.is_valid():
            lecturer_opinion: LecturerOpinion = form.save(commit=False)
            lecturer_opinion.lecturer = lecturer
            lecturer_opinion.added_on_website = True
            lecturer_opinion.save()

            todo_url = reverse(
                "admin:core_lectureropinion_change",
                kwargs={"object_id": lecturer_opinion.id},  # type: ignore
            )
            create_crm_todo(
                f"Przesłano opinie o wykładowcy `{lecturer.fullname}`",
                "Zatwierdź lub zignoruj opinie",
                "message-text-2",
                "warning",
                f"{todo_url}",
            )

            return redirect(
                reverse(
                    "core:lecturer_opinion_thanks",
                    kwargs={"slug": lecturer.slug},
                )
            )
    else:
        form = LecturerOpinionForm(initial={"rating": "5stars"})

    return TemplateResponse(
        request,
        template_name,
        {
            "form": form,
            "lecturer": lecturer,
            "tabs": service.get_lecturer_tabs(-1),
        },
    )
