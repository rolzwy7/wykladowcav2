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
from core.forms.widgets import (
    ApplicationTypeWidget,
    CheckboxWidget,
    EmailFloatingInputWidget,
    TextFloatingInputWidget,
)
from core.models import (
    WebinarApplication,
    WebinarApplicationCompany,
    WebinarApplicationInvoice,
    WebinarApplicationPrivatePerson,
    WebinarApplicationSubmitter,
    WebinarParticipant,
)


class ApplicationTypeForm(ModelForm):
    """Type form for webinar application"""

    class Meta:
        model = WebinarApplication
        fields = ["application_type"]
        widgets = {"application_type": ApplicationTypeWidget()}


class ApplicationCompanyForm(ModelForm):
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
        model = WebinarApplicationCompany
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
            "nip": TextInput(attrs={"class": "form-control"}),
            "name": TextInput(attrs={"class": "form-control"}),
            "address": TextInput(attrs={"class": "form-control"}),
            "postal_code": TextInput(
                attrs={"class": "form-control", "placeholder": "__-___"}
            ),
            "city": TextInput(attrs={"class": "form-control"}),
            "email": EmailInput(attrs={"class": "form-control"}),
            "phone_number": TextInput(attrs={"class": "form-control"}),
        }


class ApplicationPersonDetailForm(ModelForm):
    """Invoice form for webinar application"""

    def clean_email(self):
        """Clean email"""
        email = self.cleaned_data["email"]
        return email.lower()

    class Meta:
        model = WebinarApplicationPrivatePerson
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
            "first_name": TextFloatingInputWidget(attrs={"label": "Imię"}),
            "last_name": TextFloatingInputWidget(attrs={"label": "Nazwisko"}),
            "address": TextFloatingInputWidget(attrs={"label": "Adres"}),
            "postal_code": TextFloatingInputWidget(
                attrs={"label": "Kod pocztowy"}
            ),
            "city": TextFloatingInputWidget(attrs={"label": "Miejscowość"}),
            "email": EmailFloatingInputWidget(attrs={"label": "Adres E-mail"}),
            "phone": TextFloatingInputWidget(attrs={"label": "Numer telefonu"}),
        }


class ApplicationInvoiceForm(ModelForm):
    """Invoice form for webinar application"""

    def clean_invoice_email(self):
        """Clean email"""
        invoice_email = self.cleaned_data["invoice_email"]
        return invoice_email.lower()

    class Meta:
        model = WebinarApplicationInvoice
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
        self.fields[
            "vat_exemption"
        ].choices = ALLOWED_EXEMPTIONS_BY_APPLICATION_TYPE[application_type]


class ApplicationSubmitterForm(ModelForm):
    """Submitter form for webinar application"""

    def clean_email(self):
        """Clean email"""
        email = self.cleaned_data["email"]
        return email.lower()

    class Meta:
        model = WebinarApplicationSubmitter
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "is_participant",
        ]
        widgets = {
            "is_participant": CheckboxWidget(
                attrs={
                    "label": (
                        "Kliknij tutaj jeśli osoba zgłaszająca"
                        " jest też uczestnikiem szkolenia"
                    )
                }
            ),
            "first_name": TextInput(attrs={"class": "form-control"}),
            "last_name": TextInput(attrs={"class": "form-control"}),
            "email": EmailInput(attrs={"class": "form-control"}),
            "phone": TextInput(attrs={"class": "form-control"}),
        }


class ApplicationParticipantForm(ModelForm):
    """Participant form for webinar application"""

    first_name = CharField(
        required=True, widget=TextInput(attrs={"class": "form-control"})
    )
    last_name = CharField(
        required=True, widget=TextInput(attrs={"class": "form-control"})
    )
    email = CharField(
        required=True, widget=EmailInput(attrs={"class": "form-control"})
    )
    phone = CharField(
        required=True, widget=TextInput(attrs={"class": "form-control"})
    )

    def clean_email(self):
        """Clean email"""
        email = self.cleaned_data["email"]
        return email.lower()

    class Meta:
        model = WebinarParticipant
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
        ]
        # widgets = {
        #     "first_name": TextInput(attrs={"class": "form-control"}),
        #     "last_name": TextInput(attrs={"class": "form-control"}),
        #     "email": EmailInput(attrs={"class": "form-control"}),
        #     "phone": TextInput(attrs={"class": "form-control"}),
        # }


class ApplicationAdditionalInformationForm(ModelForm):
    """Additional information form for webinar application"""

    class Meta:
        model = WebinarApplication
        fields = [
            "additional_information",
        ]
        widgets = {
            "additional_information": Textarea(attrs={"class": "form-control"})
        }


class ApplicationSummarySubmitForm(Form):
    """Summary submit form for webinar application"""

    accept_terms_of_service = CharField(
        widget=CheckboxWidget(
            attrs={
                "label": ("Kliknij tutaj, aby zaakceptować regulamin szkoleń")
            }
        )
    )
