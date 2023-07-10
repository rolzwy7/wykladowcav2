from django.conf import settings
from django.http import HttpRequest


def company(request: HttpRequest):
    """Company context processor"""
    return {
        "COMPANY_NAME": settings.COMPANY_NAME,
        "COMPANY_NAME_FULL": settings.COMPANY_NAME_FULL,
        "COMPANY_NIP": settings.COMPANY_NIP,
        "COMPANY_REGON": settings.COMPANY_REGON,
        "COMPANY_CITY": settings.COMPANY_CITY,
        "COMPANY_POSTAL_CODE": settings.COMPANY_POSTAL_CODE,
        "COMPANY_STREET": settings.COMPANY_STREET,
        "COMPANY_ADDRESS": settings.COMPANY_ADDRESS,
        "COMPANY_BANK_ACCOUNT_NUMBER": settings.COMPANY_BANK_ACCOUNT_NUMBER,
        "COMPANY_BANK_SWIFT": settings.COMPANY_BANK_SWIFT,
        "COMPANY_BANK_NAME": settings.COMPANY_BANK_NAME,
        "COMPANY_OWNER_SIGNATURE": settings.COMPANY_OWNER_SIGNATURE,
        "COMPANY_REGISTER_TYPE": settings.COMPANY_REGISTER_TYPE,
        "COMPANY_REGISTER_UNIT": settings.COMPANY_REGISTER_UNIT,
        "COMPANY_FAX": settings.COMPANY_FAX,
        "COMPANY_OFFICE_EMAIL": settings.COMPANY_OFFICE_EMAIL,
        "COMPANY_OFFICE_PHONE": settings.COMPANY_OFFICE_PHONE,
        "COMPANY_WWW": settings.COMPANY_WWW,
    }
