"""CRM crm_webinar_bulk_duplicate"""

# flake8: noqa=E501
from django import forms
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts.requests_consts import POST
from core.models import Webinar
from core.models.enums import WebinarStatus


class WebinarForm(forms.ModelForm):
    """WebinarForm"""

    class Meta:
        """Meta"""

        model = Webinar
        fields = ["is_fake", "is_hidden", "price_netto", "date"]


def crm_webinar_bulk_duplicate(request, pk):
    """crm_webinar_bulk_duplicate"""
    template_name = "core/pages/crm/webinar/CrmWebinarBulkDuplicate.html"
    webinar = get_object_or_404(Webinar, pk=pk)

    if request.GET.get("extra"):
        extra = int(request.GET["extra"])
    else:
        extra = 0

    WebinarFormSet = modelformset_factory(  # pylint: disable=invalid-name
        Webinar, form=WebinarForm, extra=extra
    )

    if request.method == POST:
        formset = WebinarFormSet(request.POST)
        for form in formset:
            form.is_valid()
            is_fake = form.cleaned_data["is_fake"]
            is_hidden = form.cleaned_data["is_hidden"]
            price_netto = form.cleaned_data["price_netto"]
            date = form.cleaned_data["date"]

            webinar: Webinar = Webinar.manager.get(pk=pk)
            temp_categories = [_ for _ in webinar.categories.all()]
            webinar.id = None  # type: ignore
            webinar.is_fake = is_fake
            webinar.is_hidden = is_hidden
            webinar.price_netto = price_netto
            webinar.date = date
            webinar.slug = ""
            webinar.status = WebinarStatus.INIT
            webinar.save()
            for cat in temp_categories:
                webinar.categories.add(cat)
        return redirect(reverse("core:crm_upcoming_webinars"))
    else:
        formset = WebinarFormSet(
            queryset=Webinar.manager.filter(pk=pk),
            initial=[
                {
                    "is_fake": webinar.is_fake,
                    "is_hidden": webinar.is_hidden,
                    "price_netto": webinar.price_netto,
                    "date": webinar.date,
                }
                for _ in range(extra)
            ],
        )

    return TemplateResponse(
        request, template_name, {"webinar": webinar, "formset": formset, "extra": extra}
    )
