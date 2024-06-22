"""
Create invoice for application in Fakturownia
"""

# flake8: noqa=E501
# pylint: disable=line-too-long
# pylint: disable=import-outside-toplevel
import requests
from django.conf import settings
from django.template.defaultfilters import date as _date
from django.utils.timezone import now, timedelta
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.consts.exemptions_consts import VAT_EXEMPTIONS_LEGAL_BASIS, VAT_VALUE_PERCENT
from core.models import (
    Webinar,
    WebinarApplication,
    WebinarApplicationInvoice,
    WebinarParticipant,
)


class InvoiceCreateResult(BaseModel):
    """Excerpt of result of invoice creation in Fakturownia"""

    invoice_id: int  # id
    invoice_number: str  # number
    invoice_view_url: str  # view_url


def create_invoice_for_application(
    application: WebinarApplication,
) -> InvoiceCreateResult:
    """Create new invoice in Fakturownia"""

    # Get webinar and it's ID
    webinar: Webinar = application.webinar
    webinar_id: int = webinar.id  # type: ignore

    # Get invoice and invoice (buyer) e-mail
    invoice: WebinarApplicationInvoice = application.invoice  # type: ignore
    buyer_email = invoice.invoice_email

    # Define buyer data (company or private person)
    buyer_data = {}

    # Set buyer data for campany if set
    if application.buyer:
        _buyer = application.buyer
        buyer_data = {
            "buyer_name": _buyer.name,
            "buyer_tax_no_kind": "NIP",
            "buyer_tax_no": _buyer.nip,
            "buyer_post_code": _buyer.postal_code,
            "buyer_city": _buyer.city,
            "buyer_street": _buyer.address,
            "buyer_email": buyer_email,
        }

    # Override (company) buyer data if private person is set
    if application.private_person:
        _private_person = application.private_person
        buyer_data = {
            "buyer_company": False,
            "buyer_person": _private_person.fullname,
            "buyer_first_name": _private_person.first_name,
            "buyer_last_name": _private_person.last_name,
            "buyer_post_code": _private_person.postal_code,
            "buyer_city": _private_person.city,
            "buyer_street": _private_person.address,
            "buyer_email": buyer_email,
        }

    # Get recipient data if set
    recipient_data = {}
    if application.recipient:
        _recipient = application.recipient
        recipient_data = {
            "recipient_name": _recipient.name,
            "recipient_street": _recipient.address,
            "recipient_post_code": _recipient.postal_code,
            "recipient_city": _recipient.city,
        }

    # Get valid participants for this applications
    valid_participants_count = (
        WebinarParticipant.manager.get_valid_participants_for_application(
            application=application
        ).count()
    )

    # Sell date is a date of the webinar
    sell_date = _date(webinar.date, "Y-m-d")

    # Issue date is now
    issue_date = _date(now(), "Y-m-d")

    # Payment deadline is webinar date + INVOICE_DEADLINE_DAYS setting
    payment_to = _date(
        webinar.date + timedelta(days=settings.INVOICE_DEADLINE_DAYS), "Y-m-d"
    )

    # Add extra data if neccessary
    extra_data = {}

    # Add text adnotation about tax exempt reason
    if invoice.is_vat_exempt:
        extra_data["exempt_tax_kind"] = VAT_EXEMPTIONS_LEGAL_BASIS.get(
            invoice.vat_exemption, "Zwolnienie z VAT"
        )

    # Add invoice description if set
    if invoice.invoice_additional_info:
        extra_data["description"] = invoice.invoice_additional_info

    payload = {
        "api_token": settings.FAKTUROWNIA_API_KEY,
        "invoice": {
            **extra_data,
            "kind": "vat",
            # Dates
            "sell_date": sell_date,
            "issue_date": issue_date,
            "payment_to": payment_to,
            # Seller
            "seller_name": settings.COMPANY_NAME_FULL,
            "seller_tax_no": settings.COMPANY_NIP,
            "seller_tax_no_kind": "NIP",
            "seller_bank_account": settings.COMPANY_BANK_ACCOUNT_NUMBER,
            "seller_bank": settings.COMPANY_BANK_NAME,
            "seller_post_code": settings.COMPANY_POSTAL_CODE,
            "seller_city": settings.COMPANY_CITY,
            "seller_street": settings.COMPANY_STREET,
            "seller_country": "PL",
            "seller_phone": settings.COMPANY_OFFICE_PHONE,
            # Buyer
            **buyer_data,
            # Recipient
            **recipient_data,
            "gtu_codes": ["GTU_12"],
            "positions": [
                {
                    "name": webinar.title_original,
                    "quantity": valid_participants_count,
                    "quantity_unit": "os.",
                    "code": f"webinar{webinar_id}",
                    "gtu_code": "GTU_12",
                    "tax": "zw" if invoice.is_vat_exempt else VAT_VALUE_PERCENT,
                    "total_price_gross": round(
                        application.price_brutto * valid_participants_count, 2
                    ),
                }
            ],
        },
    }

    response = requests.request(
        "POST",
        f"{settings.FAKTUROWNIA_API_URL}/invoices.json",
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=15,
    )

    response.raise_for_status()
    result_json = response.json()

    return InvoiceCreateResult(
        invoice_id=result_json["id"],
        invoice_number=result_json["number"],
        invoice_view_url=result_json["view_url"],
    )
