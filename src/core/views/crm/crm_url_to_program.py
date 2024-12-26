"""crm_url_to_program"""

# flake8: noqa=E501

from django.forms import Form, TextInput, URLField
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts.requests_consts import POST
from core.libs.konkurencja.flightcontrol import konkurencja_fetcher
from core.models import Webinar


class UrlForm(Form):
    """UrlForm"""

    url = URLField(required=True, widget=TextInput(attrs={"class": "form-control"}))


def crm_url_to_program(request, pk):
    """crm_url_to_program"""
    template_name = "core/pages/crm/webinar/CrmUrlToProgram.html"
    webinar = get_object_or_404(Webinar, pk=pk)
    webinar_id: int = webinar.id  # type: ignore

    if request.method == POST:
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]

            try:
                fetcher = konkurencja_fetcher(url)
            except Exception as e:
                return HttpResponse(f"{e}", content_type="text/html; charset=utf-8")

            try:
                program = fetcher.get_program()
                if program:
                    webinar.program = program
                    webinar.save()
                else:
                    return HttpResponse(
                        "Strona została pobrana, ale nie udało się przetworzyć programu",
                        content_type="text/html; charset=utf-8",
                    )
            except Exception as e:
                return HttpResponse(f"{e}", content_type="text/html; charset=utf-8")

            # Handle the URL as needed
            return redirect(
                reverse("admin:core_webinar_change", kwargs={"object_id": webinar_id})
            )
    else:
        form = UrlForm()

    return TemplateResponse(request, template_name, {"webinar": webinar, "form": form})
