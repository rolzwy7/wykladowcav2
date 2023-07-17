from string import digits

from django.conf import settings

from core.libs.fakturownia import download_invoice
from core.libs.notifications.email import (
    EmailMessage,
    EmailTemplate,
    email_get_application_context,
)
from core.models import WebinarApplication, WebinarApplicationMetadata

COMPANY_NAME = settings.COMPANY_NAME


def send_invoice_email(email: str, application_id: int):
    """Send invoice email"""

    # Get application and it's metadata
    application = WebinarApplication.manager.get(id=application_id)
    metadata = WebinarApplicationMetadata.objects.get(application=application)

    # Get invoice number
    invoice_number = metadata.invoice_number

    attachment_name = "Faktura_"
    for char in invoice_number:
        attachment_name += char if char in digits else "_"
    attachment_name += "_Wykladowca_pl.pdf"

    # Download invoice PDF (bytes) from API
    invoice_content: bytes = download_invoice(metadata.invoice_id)

    # Prepare email message
    email_template = EmailTemplate(
        "email/EmailInvoice.html",
        {
            "invoice_number": invoice_number,
            **email_get_application_context(application_id),
        },
    )
    email_message = EmailMessage(
        email_template,
        f"Faktura {invoice_number} za udział w szkoleniu - {COMPANY_NAME}",
        email,
    )
    email_message.attach(attachment_name, invoice_content, "application/pdf")
    email_message.send()
