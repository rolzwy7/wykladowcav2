"""CRM Word To Program Text"""

# flake8: noqa=E501

from django import forms
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from markdown import markdown

from core.consts.requests_consts import POST
from core.libs.html_operations.program import tabowanie_to_html
from core.models import Webinar


class ProgramTextForm(forms.ModelForm):

    class Meta:
        model = Webinar
        fields = ["program_word_text"]
        widgets = {
            "program_word_text": forms.Textarea(
                attrs={"class": "form-control", "cols": "40", "rows": "200"}
            )
        }


def crm_program_text_manual_adjust(request, pk):
    """crm_word_to_program_text"""
    template_name = "core/pages/crm/webinar/CrmProgramTextManualAdjust.html"
    webinar = get_object_or_404(Webinar, pk=pk)

    if request.method == POST:
        form = ProgramTextForm(request.POST, instance=webinar)
        if form.is_valid():

            webinar: Webinar = form.save(commit=False)
            webinar.program = tabowanie_to_html(webinar.program_word_text)
            webinar.save()

            return redirect(
                reverse(
                    "core:webinar_redirect_to_program",
                    kwargs={"pk": webinar.pk},
                )
            )

            # Add any additional processing or redirection here
    else:
        form = ProgramTextForm(instance=webinar)

    return TemplateResponse(request, template_name, {"webinar": webinar, "form": form})
