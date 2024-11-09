"""
Mailing sending procedure
"""

# flake8: noqa:E501
# pylint: disable=global-variable-not-assigned
# pylint: disable=broad-exception-caught
# pylint: disable=unused-variable
# pylint: disable=invalid-name

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import WebinarApplicationMetadata
from core.models.enums.webinar_enums import WebinarStatus
from core.models.webinar_model import Webinar


class Command(BaseCommand):
    """update_fakturownia_categories"""

    help = "update_fakturownia_categories"

    def add_arguments(self, parser): ...

    def handle(self, *args, **options):
        """handle"""

        print(settings.FAKTUROWNIA_API_URL)

        webinar_metadatas = WebinarApplicationMetadata.objects.all()

        for webinar_metadata in webinar_metadatas:
            webinar: Webinar = webinar_metadata.application.webinar
            invoice_id: str = webinar_metadata.invoice_id
            print("\n", webinar_metadata.id, invoice_id, webinar, webinar.status)

            if webinar.status != WebinarStatus.DONE:
                print("Webinar is not DONE")
                continue

            if not invoice_id:
                print("Invoice id is not set")
                continue

            first_main_category_fakturownia_id = ""
            for category in webinar.categories.all():
                first_main_category_fakturownia_id = category.fakturownia_category_id
                break

            if not first_main_category_fakturownia_id:
                print("No main category found with filled faktrownia cat id")
                continue

            print("Fakturownia id:", first_main_category_fakturownia_id)

            response = requests.get(
                f"{settings.FAKTUROWNIA_API_URL}/invoices/{invoice_id}.json?api_token={settings.FAKTUROWNIA_API_KEY}",
                timeout=10,
            )

            if response.json()["category_id"] is not None:
                print("Category id is already set")
                continue
            else:
                print("Category id is not set -> setting")
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
                data = {
                    "api_token": settings.FAKTUROWNIA_API_KEY,
                    "invoice": {"category_id": first_main_category_fakturownia_id},
                }
                response = requests.put(
                    f"{settings.FAKTUROWNIA_API_URL}/invoices/{invoice_id}.json",
                    headers=headers,
                    json=data,
                    timeout=10,
                )
                print(response.json())
