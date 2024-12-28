"""crm_webinar_new_from_url"""

# flake8: noqa=E501

from django.forms import Form, TextInput, URLField
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import now

from core.consts.requests_consts import POST
from core.libs.konkurencja.flightcontrol import (
    KONKURENCJA_FETCHERS,
    konkurencja_fetcher,
)
from core.models import Lecturer, Webinar, WebinarMetadata
from core.models.enums.webinar_enums import WebinarStatus


class UrlForm(Form):
    """UrlForm"""

    url = URLField(required=True, widget=TextInput(attrs={"class": "form-control"}))


def crm_webinar_new_from_url(request):
    """crm_webinar_new_from_url"""
    template_name = "core/pages/crm/webinar/CrmWebinarNewFromUrl.html"

    if request.method == POST:
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]

            try:
                konkurencja, fetcher = konkurencja_fetcher(url)
            except Exception as e:
                return HttpResponse(f"{e}", content_type="text/html; charset=utf-8")

            title = fetcher.get_title()
            date = fetcher.get_date()
            lecturer = fetcher.get_lecturer()
            price = fetcher.get_price()
            program = fetcher.get_program()

            webinar = Webinar(
                status=WebinarStatus.DRAFT,
                date=(
                    date
                    if date
                    else now().replace(hour=10, minute=0, second=0, microsecond=0)
                ),
                title_original=title if title else "Błąd pobierania tytułu",
                title=title[:220] if title else "Błąd pobierania tytułu",
                price_netto=price if price else 999,
                lecturer=Lecturer.manager.all().first(),
                program=program if program else "Błąd pobierania programu",
            )
            webinar.save()
            webinar_id: int = webinar.id  # type: ignore

            metadata = WebinarMetadata.objects.get(  # pylint: disable=no-member
                webinar=webinar
            )
            metadata.fetched_from = konkurencja
            metadata.fetched_from_url = url
            metadata.fetched_too_long_title = (
                True if title and len(title) > 220 else False
            )
            metadata.save()
            return redirect(
                reverse("admin:core_webinar_change", kwargs={"object_id": webinar_id})
            )
    else:
        form = UrlForm()

    supported_konkurencja = [
        (kname, ktuple[0]) for kname, ktuple in KONKURENCJA_FETCHERS.items()
    ]

    return TemplateResponse(
        request,
        template_name,
        {"form": form, "supported_konkurencja": supported_konkurencja},
    )
