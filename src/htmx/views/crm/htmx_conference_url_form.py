"""htmx_conference_url_form"""

# flake8: noqa=E501

from django.forms import ModelForm, TextInput
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.template.response import TemplateResponse

from core.consts import POST
from core.models import ConferenceEdition


class ConferenceUrlForm(ModelForm):
    """ConferenceUrlForm"""

    class Meta:
        """meta"""

        model = ConferenceEdition
        fields = ["stream_url_page"]
        widgets = {
            "stream_url_page": TextInput(attrs={"class": "form-control"}),
        }


def htmx_conference_url_form(request: HttpRequest, pk: int, mode: str):
    """htmx_conference_url_form"""
    template_path = "htmx/conference_url_form/form.html"
    edition = get_object_or_404(ConferenceEdition, pk=pk)
    context = {"edition": edition}

    def get_result():
        return TemplateResponse(
            request,
            "htmx/conference_url_form/result.html",
            {**context},
        )

    if mode == "result":
        return get_result()

    if request.method == POST:
        form = ConferenceUrlForm(request.POST, instance=edition)
        if form.is_valid():
            form.save()
        return get_result()

    return TemplateResponse(
        request,
        template_path,
        {**context, "form": ConferenceUrlForm(instance=edition)},
    )
