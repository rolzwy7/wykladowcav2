"""crm_mailing_schedule_mailing"""

# flake8: noqa=E501

from django import forms
from django.forms import DateInput, DateTimeInput, Select, Textarea, TextInput
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import now, timedelta

from core.consts.requests_consts import POST
from core.libs.mailing.export import export_emails_mongo_index_tags
from core.models import Webinar
from core.models.mailing import MailingScheduled


class MailingScheduledForm(forms.ModelForm):
    """Form for MailingScheduled model"""

    class Meta:
        model = MailingScheduled
        fields = [
            "smtp_sender",
            "target_date",
            "schedule_after",
            "target_code",
            "url",
            "title",
            "subjects",
            "alias",
            "resignation_list",
        ]

        widgets = {
            "smtp_sender": Select(attrs={"class": "form-control"}),
            "target_date": DateInput(attrs={"class": "form-control"}),
            "schedule_after": DateTimeInput(attrs={"class": "form-control"}),
            "target_code": TextInput(attrs={"class": "form-control"}),
            "url": TextInput(attrs={"class": "form-control"}),
            "title": TextInput(attrs={"class": "form-control"}),
            "subjects": Textarea(attrs={"class": "form-control"}),
            "alias": TextInput(attrs={"class": "form-control"}),
            "resignation_list": TextInput(attrs={"class": "form-control"}),
        }


def crm_mailing_schedule_mailing(request, pk):
    """crm_mailing_schedule_mailing"""
    template_name = "core/pages/crm/mailing/MailingSchedule.html"

    webinar = get_object_or_404(Webinar, pk=pk)
    webinar_id: int = webinar.id  # type: ignore

    index_tags = export_emails_mongo_index_tags()

    if request.method == POST:
        form = MailingScheduledForm(request.POST)
        if form.is_valid():

            tags = list(
                set(
                    sorted(
                        [
                            *request.POST.getlist("mongo_db"),
                            *request.POST.getlist("dobicie"),
                        ]
                    )
                )
            )

            schedule = MailingScheduled(
                smtp_sender=form.cleaned_data["smtp_sender"],
                webinar=webinar,
                schedule_after=form.cleaned_data["schedule_after"],
                target_date=form.cleaned_data["target_date"],
                target_code=form.cleaned_data["target_code"],
                url=form.cleaned_data["url"],
                title=form.cleaned_data["title"],
                subjects=form.cleaned_data["subjects"],
                alias=form.cleaned_data["alias"],
                resignation_list=form.cleaned_data["resignation_list"],
                tags="\n".join(tags),
            )
            schedule.save()

            return redirect(reverse("core:crm_mailing_campaigns_list"))
    else:
        schedule_after = webinar.date - timedelta(days=1)
        schedule_after = schedule_after.replace(
            hour=16, minute=30, second=0, microsecond=0
        )
        form = MailingScheduledForm(
            initial={
                "title": f"{now().strftime('%Y%m%d')}_SCHEDULE_WEB_{webinar_id}_",
                "alias": webinar.lecturer.fullname,
                "subjects": webinar.title,
                "target_date": webinar.date.date(),
                "schedule_after": schedule_after,
            }
        )

    return TemplateResponse(
        request,
        template_name,
        {"webinar": webinar, "tags": index_tags, "form": form},
    )
