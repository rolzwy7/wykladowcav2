"""CRM Word To Program Text"""

# flake8: noqa=E501

from django import forms
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from docx import Document

from core.consts.requests_consts import POST
from core.models import Webinar


class WordUploadForm(forms.Form):
    """WordUploadForm"""

    word_file = forms.FileField(label="Wybierz plik Word z programem")


def convert_word_to_text(docx_bytes):
    """convert_word_to_text"""
    ret = ""

    try:
        # Load the Word document
        doc = Document(docx_bytes)

        # Extract all text from the document
        for paragraph in doc.paragraphs:
            ret += paragraph.text.strip() + "\n"

    except Exception as e:
        return f"Błąd: {e}"

    return ret


def crm_word_to_program_text(request, pk):
    """crm_word_to_program_text"""
    template_name = "core/pages/crm/webinar/CrmWordToProgramText.html"
    webinar = get_object_or_404(Webinar, pk=pk)

    if request.method == POST:
        form = WordUploadForm(request.POST, request.FILES)
        if form.is_valid():
            word_file = form.cleaned_data["word_file"]
            webinar.program_word_text = convert_word_to_text(word_file)
            webinar.save()
            return redirect(
                reverse(
                    "core:crm_program_text_manual_adjust", kwargs={"pk": webinar.pk}
                )
            )
    else:
        form = WordUploadForm()

    return TemplateResponse(request, template_name, {"form": form, "webinar": webinar})
