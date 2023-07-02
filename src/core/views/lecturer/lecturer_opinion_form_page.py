from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import LecturerOpinionForm
from core.models import Lecturer
from core.services.lecturer_service import LecturerService
from core.tasks.create_crm_todo.procedure import create_crm_todo


def lecturer_opinion_form_page(request, slug: str):
    template_name = "core/pages/lecturer/LecturerOpinionFormPage.html"
    lecturer = get_object_or_404(Lecturer, slug=slug)
    service = LecturerService(lecturer)

    if request.method == POST:
        form = LecturerOpinionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.lecturer = lecturer
            instance.save()

            todo_url = reverse(
                "admin:core_lectureropinion_change",
                kwargs={"object_id": instance.id},
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
        form = LecturerOpinionForm()

    return TemplateResponse(
        request,
        template_name,
        {
            "form": form,
            "lecturer": lecturer,
            "tabs": service.get_lecturer_tabs(-1),
        },
    )
