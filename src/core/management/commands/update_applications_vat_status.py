"""
Mailing sending procedure
"""

# flake8: noqa:E501
# pylint: disable=global-variable-not-assigned
# pylint: disable=broad-exception-caught
# pylint: disable=unused-variable
# pylint: disable=invalid-name

import requests
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.timezone import now

from core.models.enums.application_enums import ApplicationStatus
from core.models.enums.webinar_enums import WebinarApplicationType
from core.models.webinar_application_model import (
    WebinarApplication,
    WebinarApplicationMetadata,
)


class Command(BaseCommand):
    """Mailing clean"""

    help = "Update applications VAT status"

    def add_arguments(self, parser): ...

    def handle(self, *args, **options):
        """handle"""

        applications = WebinarApplication.manager.filter(
            ~Q(application_type=WebinarApplicationType.PRIVATE_PERSON)
            & (Q(status=ApplicationStatus.SENT) | Q(status=ApplicationStatus.PAYED))
        ).order_by("-created_at")

        for application in applications:
            print("Procesuje zgłoszenie id=", application.id)
            metadata = WebinarApplicationMetadata.objects.get(application=application)
            if metadata.vat_status:
                print("Already has vat status:", application)
                continue

            ts = now().date().strftime("%Y-%m-%d")
            nip = application.buyer.nip
            url = f"https://wl-api.mf.gov.pl/api/search/nip/{nip}?date={ts}"

            print("\n")
            print(
                application,
                metadata,
                nip,
                ts,
            )
            print(url)

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                json_data = response.json()
            except requests.HTTPError as e:  # raise_for_status
                raise
            else:
                try:
                    vat_status = json_data["result"]["subject"]["statusVat"]
                except Exception as e:
                    vat_status = "Błąd result->subject->statusVat"
                print(vat_status)
                WebinarApplicationMetadata.objects.filter(
                    application=application
                ).update(vat_status=vat_status)
