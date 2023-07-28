from django.forms import CharField, Form, ModelForm

from core.consts import ALLOWED_EXEMPTIONS_BY_APPLICATION_TYPE
from core.forms.widgets import (
    ApplicationTypeWidget,
    CheckboxWidget,
    EmailFloatingInputWidget,
    SelectFloatingInputWidget,
    TextareaFloatingInputWidget,
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
        return nip.replace("-", "").replace(" ", "")

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
            "nip": TextFloatingInputWidget(attrs={"label": "NIP"}),
            "name": TextFloatingInputWidget(attrs={"label": "Nazwa płatnika"}),
            "address": TextFloatingInputWidget(attrs={"label": "Adres"}),
            "postal_code": TextFloatingInputWidget(
                attrs={"label": "Kod pocztowy"}
            ),
            "city": TextFloatingInputWidget(attrs={"label": "Miejscowość"}),
            "email": TextFloatingInputWidget(
                attrs={"label": "Adres E-mail (opjonalnie)"}
            ),
            "phone_number": TextFloatingInputWidget(
                attrs={"label": "Numer telefonu (opjonalnie)"}
            ),
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
            "invoice_type": SelectFloatingInputWidget(
                attrs={"label": "Typ faktury"}
            ),
            "invoice_email": EmailFloatingInputWidget(
                attrs={"label": "E-mail (na który zostanie wysłana faktura)"}
            ),
            # "invoice_additional_info": TextareaFloatingInputWidget(
            #     attrs={"label": "Dodatkowe informacje (widoczne na fakturze)"}
            # ),
            "vat_exemption": SelectFloatingInputWidget(
                attrs={"label": "Zwolnienie z VAT"}
            ),
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
                        " jest też uczestnikiem webinaru"
                    )
                }
            ),
            "first_name": TextFloatingInputWidget(attrs={"label": "Imię"}),
            "last_name": TextFloatingInputWidget(attrs={"label": "Nazwisko"}),
            "email": EmailFloatingInputWidget(attrs={"label": "Adres E-mail"}),
            "phone": TextFloatingInputWidget(attrs={"label": "Numer telefonu"}),
        }


class ApplicationParticipantForm(ModelForm):
    """Participant form for webinar application"""

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
        widgets = {
            "first_name": TextFloatingInputWidget(attrs={"label": "Imię"}),
            "last_name": TextFloatingInputWidget(attrs={"label": "Nazwisko"}),
            "email": EmailFloatingInputWidget(attrs={"label": "Adres E-mail"}),
            "phone": TextFloatingInputWidget(
                attrs={"label": "Numer telefonu (opcjonalnie)"}
            ),
        }


class ApplicationAdditionalInformationForm(ModelForm):
    """Additional information form for webinar application"""

    class Meta:
        model = WebinarApplication
        fields = [
            "additional_information",
        ]
        widgets = {
            "additional_information": TextareaFloatingInputWidget(
                attrs={"label": "Dodatkowe uwagi"}
            )
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
