# flake8: noqa
from .application_forms import (
    ApplicationAdditionalInformationForm,
    ApplicationBuyerForm,
    ApplicationCompanyForm,
    ApplicationInvoiceForm,
    ApplicationParticipantForm,
    ApplicationPersonDetailForm,
    ApplicationRecipientForm,
    ApplicationSubmitterForm,
    ApplicationSummarySubmitForm,
    ApplicationTypeForm,
)
from .conference_forms import ConferenceFreeParticipantModelForm
from .contact_message_form import ContactMessageForm
from .discount_forms import DiscountCodeForm
from .lecturer_forms import LecturerOpinionForm
from .login_form import LoginForm
from .loyalty_forms import LoyaltyPayoutRequestForm
from .mailing_forms import (
    MailingAddEmailsForm,
    MailingAreYouSureForm,
    MailingSendTestEmailForm,
)
from .registration_form import RegistrationForm
from .resignation_forms import ResignationForm
from .sale_recording_application_forms import (
    SaleRecordingApplicationAdditionalInformationForm,
    SaleRecordingApplicationBuyerForm,
    SaleRecordingApplicationInvoiceForm,
    SaleRecordingApplicationParticipantForm,
    SaleRecordingApplicationPersonDetailForm,
    SaleRecordingApplicationRecipientForm,
    SaleRecordingApplicationSummarySubmitForm,
    SaleRecordingApplicationTypeForm,
)
from .tagging_forms import TaggingAddEmailsForm
from .webinar_asset_forms import WebinarAssetForm
