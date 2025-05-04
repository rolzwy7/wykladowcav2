"""Application forms"""

# flake8: noqa=E501

from django.forms import (
    CharField,
    EmailInput,
    Form,
    HiddenInput,
    ModelForm,
    Select,
    Textarea,
    TextInput,
)

from core.consts import ALLOWED_EXEMPTIONS_BY_APPLICATION_TYPE
from core.forms.widgets import ApplicationTypeWidget, CheckboxWidget
from core.models import (
    SaleRecordingApplication,
    SaleRecordingApplicationCompany,
    SaleRecordingApplicationInvoice,
    SaleRecordingApplicationPrivatePerson,
    SaleRecordingParticipant,
)

# from django.forms import (
#     BooleanField,
#     CharField,
#     EmailInput,
#     Form,
#     HiddenInput,
#     ModelForm,
#     Select,
#     Textarea,
#     TextInput,
# )


class SaleRecordingApplicationTypeForm(ModelForm):
    """Type form for sale recording application"""

    class Meta:
        model = SaleRecordingApplication
        fields = ["application_type"]
        widgets = {"application_type": ApplicationTypeWidget()}


class SaleRecordingApplicationCompanyForm(ModelForm):
    """Company (buyer, recipient) form for webinar application"""

    def clean_nip(self):
        """Clean NIP number"""
        nip = self.cleaned_data["nip"]
        return nip.replace("-", "").replace(" ", "").replace("_", "")

    def clean_email(self):
        """Clean email"""
        email = self.cleaned_data["email"]
        return email.lower()

    class Meta:
        model = SaleRecordingApplicationCompany
        fields = [
            "nip",
            "name",
            "address",
            "postal_code",
            "city",
            "email",
            "phone_number",
        ]
        widgets = {
            "nip": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Numer NIP, np. 774-00-01-454",
                }
            ),
            "name": TextInput(
                attrs={"class": "form-control", "placeholder": "Nazwa firmy"}
            ),
            "address": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ulica i numer lokalu, np. Przemysłowa 10A",
                }
            ),
            "postal_code": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Kod pocztowy, np. 45-573",
                }
            ),
            "city": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Miasto, np. Warszawa",
                }
            ),
            "email": EmailInput(attrs={"class": "form-control"}),
            "phone_number": TextInput(attrs={"class": "form-control"}),
        }


class SaleRecordingApplicationBuyerForm(SaleRecordingApplicationCompanyForm):
    """Application buyer form"""

    email = CharField(required=True, widget=TextInput(attrs={"class": "form-control"}))
    phone_number = CharField(
        required=True, widget=HiddenInput(attrs={"class": "form-control"})
    )


class SaleRecordingApplicationRecipientForm(SaleRecordingApplicationCompanyForm):
    """Application recipient form"""

    pass  # pylint: disable=unnecessary-pass


class SaleRecordingApplicationPersonDetailForm(ModelForm):
    """Invoice form for webinar application"""

    def clean_email(self):
        """Clean email"""
        email = self.cleaned_data["email"]
        return email.lower()

    class Meta:
        model = SaleRecordingApplicationPrivatePerson
        fields = [
            "first_name",
            "last_name",
            "address",
            "postal_code",
            "city",
            "email",
            "phone",
        ]
        widgets = {
            "first_name": TextInput(attrs={"class": "form-control"}),
            "last_name": TextInput(attrs={"class": "form-control"}),
            "address": TextInput(attrs={"class": "form-control"}),
            "postal_code": TextInput(attrs={"class": "form-control"}),
            "city": TextInput(attrs={"class": "form-control"}),
            "email": EmailInput(attrs={"class": "form-control"}),
            "phone": TextInput(attrs={"class": "form-control"}),
        }


class SaleRecordingApplicationInvoiceForm(ModelForm):
    """Invoice form for webinar application"""

    def clean_invoice_email(self):
        """Clean email"""
        invoice_email = self.cleaned_data["invoice_email"]
        return invoice_email.lower()

    class Meta:
        model = SaleRecordingApplicationInvoice
        fields = [
            "invoice_type",
            "invoice_email",
            # "invoice_additional_info",
            "vat_exemption",
        ]
        widgets = {
            "invoice_type": HiddenInput(attrs={"class": "form-control"}),
            "invoice_email": EmailInput(attrs={"class": "form-control"}),
            # "invoice_additional_info": TextInput(
            #     attrs={"class": "form-control"}
            # ),
            "vat_exemption": Select(attrs={"class": "form-control"}),
        }

    def set_choices(self, application_type: str):
        """Set invoice choices"""
        self.fields["vat_exemption"].choices = ALLOWED_EXEMPTIONS_BY_APPLICATION_TYPE[
            application_type
        ]


# class ApplicationSubmitterForm(ModelForm):
#     """Submitter form for webinar application"""

#     def clean_email(self):
#         """Clean email"""
#         email = self.cleaned_data["email"]
#         return email.lower()

#     class Meta:
#         model = WebinarApplicationSubmitter
#         fields = [
#             "first_name",
#             "last_name",
#             "email",
#             "phone",
#             "is_participant",
#         ]
#         widgets = {
#             "is_participant": CheckboxWidget(
#                 attrs={
#                     "label": (
#                         "Kliknij tutaj jeśli osoba zgłaszająca"
#                         " jest też uczestnikiem szkolenia"
#                     )
#                 }
#             ),
#             "first_name": TextInput(attrs={"class": "form-control"}),
#             "last_name": TextInput(attrs={"class": "form-control"}),
#             "email": EmailInput(attrs={"class": "form-control"}),
#             "phone": TextInput(attrs={"class": "form-control"}),
#         }


class SaleRecordingApplicationParticipantForm(ModelForm):
    """Participant form for webinar application"""

    first_name = CharField(
        required=True, widget=TextInput(attrs={"class": "form-control"})
    )
    last_name = CharField(
        required=True, widget=TextInput(attrs={"class": "form-control"})
    )
    email = CharField(required=True, widget=EmailInput(attrs={"class": "form-control"}))
    # access_from = CharField(
    #     required=True, widget=TextInput(attrs={"class": "form-control"})
    # )

    def clean_email(self):
        """Clean email"""
        email = self.cleaned_data["email"]
        return email.lower()

    class Meta:
        model = SaleRecordingParticipant
        # fields = ["first_name", "last_name", "email", "access_from"]
        fields = ["first_name", "last_name", "email"]
        # widgets = {
        #     "first_name": TextInput(attrs={"class": "form-control"}),
        #     "last_name": TextInput(attrs={"class": "form-control"}),
        #     "email": EmailInput(attrs={"class": "form-control"}),
        #     "phone": TextInput(attrs={"class": "form-control"}),
        # }


class SaleRecordingApplicationAdditionalInformationForm(ModelForm):
    """Additional information form for webinar application"""

    class Meta:
        model = SaleRecordingApplication
        fields = [
            "additional_information",
        ]
        widgets = {
            "additional_information": Textarea(
                attrs={"class": "form-control", "cols": "40", "rows": "5"}
            )
        }


class SaleRecordingApplicationSummarySubmitForm(Form):
    """Summary submit form for webinar application"""

    accept_terms_of_service = CharField(
        widget=CheckboxWidget(
            attrs={"label": ("Kliknij tutaj, aby zaakceptować regulamin szkoleń")}
        )
    )
