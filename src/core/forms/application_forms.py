from django.forms import ModelForm

from core.models import (
    WebinarApplication,
    WebinarApplicationCompany,
    WebinarApplicationSubmitter,
)
from core.widgets import ApplicationTypeWidget


class ApplicationTypeForm(ModelForm):
    class Meta:
        model = WebinarApplication
        fields = ["application_type"]
        widgets = {"application_type": ApplicationTypeWidget()}


class ApplicationBuyerForm(ModelForm):
    class Meta:
        model = WebinarApplicationCompany
        fields = "__all__"


class ApplicationReceiverForm(ModelForm):
    class Meta:
        model = WebinarApplicationCompany
        fields = "__all__"


class ApplicationInvoiceForm(ModelForm):
    class Meta:
        model = WebinarApplication
        fields = [
            "invoice_type",
            "invoice_email",
            "invoice_additional_info",
            "vat_exemption",
        ]


class ApplicationSubmitterForm(ModelForm):
    class Meta:
        model = WebinarApplicationSubmitter
        fields = "__all__"
