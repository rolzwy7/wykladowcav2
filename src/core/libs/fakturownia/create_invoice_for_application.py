# flake8: noqa=E501
# pylint: disable=line-too-long
# pylint: disable=import-outside-toplevel
import requests
from django.conf import settings
from django.template.defaultfilters import date as _date
from django.utils.timezone import now, timedelta
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.consts.exemptions_consts import (
    TAX_EXEMPT_TOOLTIP,
    VAT_EXEMPTION_0,
    VAT_EXEMPTION_113,
    VAT_VALUE_PERCENT,
    WE_ARE_TAX_EXEMPT,
)
from core.models import Webinar, WebinarApplication, WebinarApplicationInvoice


class InvoiceCreateResult(BaseModel):
    """Excerpt of result of invoice creation in Fakturownia"""

    invoice_id: int  # id
    invoice_number: str  # number
    invoice_view_url: str  # view_url


def create_invoice_for_application(
    application: WebinarApplication,
) -> InvoiceCreateResult:
    """Create new invoice in Fakturownia"""

    webinar: Webinar = application.webinar
    recipient = application.recipient
    buyer = application.buyer
    private_person = application.private_person
    invoice: WebinarApplicationInvoice = application.invoice  # type: ignore

    from core.services import ApplicationService

    application_service = ApplicationService(application)
    valid_participants_count = application_service.get_valid_participants().count()

    buyer_email = invoice.invoice_email  # type: ignore

    buyer_data = {}
    recipient_data = {}

    if buyer:
        buyer_data = {
            "buyer_name": buyer.name,
            "buyer_tax_no_kind": "NIP",
            "buyer_tax_no": buyer.nip,
            "buyer_post_code": buyer.postal_code,
            "buyer_city": buyer.city,
            "buyer_street": buyer.address,
            "buyer_email": buyer_email,
        }

    if private_person:
        buyer_data = {
            "buyer_company": False,
            "buyer_person": private_person.fullname,
            "buyer_first_name": private_person.first_name,
            "buyer_last_name": private_person.last_name,
            "buyer_post_code": private_person.postal_code,
            "buyer_city": private_person.city,
            "buyer_street": private_person.address,
            "buyer_email": buyer_email,
        }

    if recipient:
        recipient_data = {
            "recipient_name": recipient.name,
            "recipient_street": recipient.address,
            "recipient_post_code": recipient.postal_code,
            "recipient_city": recipient.city,
        }

    # Add text adnotation about tax exempt reason
    if WE_ARE_TAX_EXEMPT or invoice.vat_exemption == VAT_EXEMPTION_113.db_key:
        extra_data = {"exempt_tax_kind": TAX_EXEMPT_TOOLTIP}
    else:
        extra_data = {}

    # Sell date is a date of the webinar
    sell_date = _date(webinar.date, "Y-m-d")

    # Issue date is now
    issue_date = _date(now(), "Y-m-d")

    # Payment deadline is webinar date + INVOICE_DEADLINE_DAYS setting
    payment_to = _date(
        webinar.date + timedelta(days=settings.INVOICE_DEADLINE_DAYS), "Y-m-d"
    )

    seller_data = {
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
    }

    if invoice.vat_exemption == VAT_EXEMPTION_113.db_key:
        tax = "zw"
    elif invoice.vat_exemption == VAT_EXEMPTION_0.db_key:
        tax = VAT_VALUE_PERCENT
    else:
        tax = VAT_VALUE_PERCENT

    invoice_position = {
        "name": webinar.title_original,
        "quantity": valid_participants_count,
        "quantity_unit": "os.",
        "code": f"webinar{webinar.id}",  # type: ignore
        "tax": tax,
        "total_price_gross": round(
            application.price_brutto * valid_participants_count, 2
        ),
    }

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
            **seller_data,
            # Buyer
            **buyer_data,
            # Recipient
            **recipient_data,
            "positions": [invoice_position],
        },
    }

    response = requests.request(
        "POST",
        f"{settings.FAKTUROWNIA_API_URL}/invoices.json",
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=10,
    )

    response.raise_for_status()
    result_json = response.json()

    return InvoiceCreateResult(
        invoice_id=result_json["id"],
        invoice_number=result_json["number"],
        invoice_view_url=result_json["view_url"],
    )
