"""CRM crm_webinar_bulk_duplicate"""

# flake8: noqa=E501
from django import forms
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import now

from core.consts.requests_consts import POST
from core.models import Webinar, WebinarAggregate, WebinarMetadata
from core.models.enums import WebinarStatus


class WebinarForm(forms.ModelForm):
    """WebinarForm"""

    class Meta:
        """Meta"""

        model = Webinar
        fields = ["is_fake", "is_hidden", "price_netto", "date"]


def crm_webinar_bulk_duplicate(request, pk):
    """crm_webinar_bulk_duplicate"""

    original_webinar = get_object_or_404(Webinar, pk=pk)

    aggregate: WebinarAggregate = WebinarAggregate.manager.get(
        grouping_token=original_webinar.grouping_token
    )

    next_redirect = request.GET.get("next")

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

            # date = timezone.make_aware(form.cleaned_data["date"])
            date = form.cleaned_data["date"]

            # Create webinar
            webinar: Webinar = Webinar.manager.get(pk=pk)
            metadata, _ = WebinarMetadata.objects.get_or_create(webinar=webinar)
            temp_categories = [_ for _ in webinar.categories.all()]

            webinar.id = None  # type: ignore
            webinar.is_fake = is_fake
            webinar.is_hidden = is_hidden
            webinar.price_netto = price_netto
            webinar.date = date
            webinar.created_at = now()
            webinar.slug = ""
            webinar.status = WebinarStatus.INIT
            webinar.save()

            # Populate new metadata
            new_metadata, _ = WebinarMetadata.objects.get_or_create(webinar=webinar)
            new_metadata.fetched_from = metadata.fetched_from
            new_metadata.fetched_from_url = metadata.fetched_from_url
            new_metadata.fetched_too_long_title = metadata.fetched_too_long_title
            new_metadata.save()

            # Add categories
            for cat in temp_categories:
                webinar.categories.add(cat)

            metadata.save()

        if next_redirect:
            try:
                return redirect(next_redirect)
            except Exception as e:
                return redirect(reverse("core:crm_upcoming_webinars"))
        else:
            return redirect(reverse("core:crm_upcoming_webinars"))
    else:
        formset = WebinarFormSet(
            queryset=Webinar.manager.filter(pk=pk),
            initial=[
                {
                    "is_fake": original_webinar.is_fake,
                    "is_hidden": original_webinar.is_hidden,
                    "price_netto": original_webinar.price_netto,
                    "date": original_webinar.date,
                }
                for _ in range(extra)
            ],
        )

    return TemplateResponse(
        request,
        "core/pages/crm/webinar/CrmWebinarBulkDuplicate.html",
        {
            "aggregate": aggregate,
            "aggregate_categories": [cat for cat in aggregate.categories.all()],
            "webinar": original_webinar,
            "next_redirect": next_redirect,
            "formset": formset,
            "extra": extra,
            "menu": [_ for _ in range(1, 11)],
        },
    )
