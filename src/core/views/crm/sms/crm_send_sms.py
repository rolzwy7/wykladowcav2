"""CRM Send SMS"""

# flake8: noqa=E501

from django.forms import CharField, Form, Textarea, TextInput, ValidationError
from django.shortcuts import redirect
from django.template.defaultfilters import date as _date
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import get_default_timezone

from core.libs.justsend import send_sms
from core.models import WebinarParticipant


class SmsForm(Form):
    """SmsForm"""

    phone_number = CharField(
        max_length=15,
        label="Numer telefonu (9 cyfr bez spacji)",
        widget=TextInput(attrs={"class": "form-control"}),
    )

    message = CharField(
        max_length=160,
        label="Treść SMS",
        widget=Textarea(attrs={"class": "form-control"}),
    )

    def clean_phone_number(self):
        """clean_phone_number"""
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number:
            raise ValidationError("Phone number cant be None.")
        if not phone_number.isdigit():
            raise ValidationError(
                "Numer telefonu musi zawierać tylko cyfry (bez spacji itd.)"
            )
        if len(phone_number) != 9:
            raise ValidationError("Numer telefonu musi składać się z 9 cyfr")
        return phone_number


def crm_send_sms(request):
    """crm_send_sms"""
    template_name = "core/pages/crm/sms/CrmSendSMS.html"

    if request.method == "POST":
        form = SmsForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            message = form.cleaned_data["message"]

            try:
                send_sms("Wykladowca", phone_number, message)
            except Exception as e:
                return redirect(reverse("core:crm_send_sms") + f"?fail={str(e)}")
            else:
                return redirect(
                    reverse("core:crm_send_sms")
                    + f"?success_phone_number={phone_number}"
                )

    participant_id = request.GET.get("participant_id")
    if participant_id:
        participant: WebinarParticipant = WebinarParticipant.manager.get(
            id=int(participant_id)
        )
        webinar = participant.application.webinar
        tz = get_default_timezone()
        hour = _date(webinar.date.astimezone(tz), "H:i")
        default_msg = f"Przypominamy o szkoleniu dziś o {hour} - Zespół Wykladowca.pl"
        phone = "".join([ch for ch in participant.phone if ch.isdigit()])
        form = SmsForm(initial={"phone_number": phone, "message": default_msg})
    else:
        form = SmsForm()

    return TemplateResponse(
        request,
        template_name,
        {
            "form": form,
            "success_phone_number": request.GET.get("success_phone_number"),
            "fail": request.GET.get("fail"),
        },
    )
