"""CRM Word To Program Text"""

# flake8: noqa=E501

from django import forms
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from markdown import markdown

from core.consts.requests_consts import POST
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


def prepend_number_to_lines(text):
    """
    Prepends '1. ' to each line in a text, ignoring leading tabs.

    Args:
        text (str): The input text with lines.

    Returns:
        str: The updated text with '1. ' prepended to each line, respecting leading tabs.
    """
    lines = text.splitlines()
    updated_lines = []

    for line in lines:
        stripped_line = line.lstrip("\t")  # Remove leading tabs temporarily
        if stripped_line:  # Only prepend if there's content
            updated_line = f"{line[:len(line) - len(stripped_line)]}1. {stripped_line}"
        else:
            updated_line = line  # Keep empty lines or lines with only tabs as is
        updated_lines.append(updated_line)

    return "\n".join(updated_lines)


def crm_program_text_manual_adjust(request, pk):
    """crm_word_to_program_text"""
    template_name = "core/pages/crm/webinar/CrmProgramTextManualAdjust.html"
    webinar = get_object_or_404(Webinar, pk=pk)

    if request.method == POST:
        form = ProgramTextForm(request.POST, instance=webinar)
        if form.is_valid():

            webinar: Webinar = form.save(commit=False)
            webinar.program = markdown(
                "\n".join(
                    [
                        prepend_number_to_lines(line)
                        for line in webinar.program_word_text.split("\n")
                        if line.strip() != ""
                    ]
                )
            )
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
