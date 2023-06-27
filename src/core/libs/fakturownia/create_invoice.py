import requests
from django.conf import settings

# class CreateInvoiceParams():
#     ...


def create_invoice():
    """Create new invoice in Fakturownia"""
    url = f"{settings.FAKTUROWNIA_API_URL}/invoices.json"
    data = {
        "api_token": settings.FAKTUROWNIA_API_KEY,
        "invoice": {
            "kind": "vat",
            "number": None,
            "sell_date": "2023-06-27",  # application.date
            "issue_date": "2023-06-27",  # now
            "payment_to": "2023-07-04",  # application.date + 14
            "seller_name": "Seller SA",
            "seller_tax_no": "5252445767",
            "buyer_name": "Client1 SA",
            "buyer_tax_no": "5252445767",
            "positions": [
                {
                    "name": "Produkt A1",
                    "tax": 23,
                    "total_price_gross": 10.23,
                    "quantity": 1,
                },
                {
                    "name": "Produkt A2",
                    "tax": 0,
                    "total_price_gross": 50,
                    "quantity": 2,
                },
            ],
        },
    }
    try:
        result = requests.post(url, data=data, timeout=10)
        result.raise_for_status()
    except Exception as e:
        raise


# {
#     "id": 225030909,
#     "number": "1/06/2023",
#     "view_url": "https://rolzwy7.f...",
