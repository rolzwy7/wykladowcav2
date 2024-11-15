"""
This script updates invoice categories on Fakturownia for completed webinars.
"""

# flake8: noqa=E501
import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from core.consts import TelegramChats
from core.models import WebinarApplicationMetadata
from core.models.enums.webinar_enums import WebinarStatus
from core.models.webinar_model import Webinar
from core.services import TelegramService


class Command(BaseCommand):
    """
    Django management command to update Fakturownia invoice categories for webinars marked as DONE.
    """

    help = "Updates invoice categories on Fakturownia for completed webinars."

    def add_arguments(self, parser):
        # Additional arguments can be defined here if needed in the future
        pass

    def handle(self, *args, **options):
        """
        Main logic for the command execution.
        """

        telegram_service = TelegramService()

        # Display Fakturownia API URL to confirm settings
        print("Fakturownia API URL:", settings.FAKTUROWNIA_API_URL)

        # Retrieve all webinar application metadata records
        webinar_metadata_list = WebinarApplicationMetadata.objects.all()

        for metadata in webinar_metadata_list:
            # Extract related webinar and invoice information
            metadata_id: int = metadata.id  # type: ignore
            webinar: Webinar = metadata.application.webinar
            webinar_id: int = webinar.id  # type: ignore
            invoice_id = metadata.invoice_id

            print(
                f"\nMetadata ID: {metadata_id},"
                f" Webinar ID: {webinar_id},"
                f" Invoice ID: {invoice_id},"
                f" Webinar Status: {webinar.status}"
            )

            # Process only webinars that are marked as DONE
            if webinar.status != WebinarStatus.DONE:
                print("Skipping: Webinar status is not DONE.")
                continue

            # Check if an invoice ID is present
            if not invoice_id:
                print("Skipping: Invoice ID is not set.")
                input(
                    f"Zrealizowany webinar ID={webinar_id} nie ma podłączonej faktury"
                )
                # telegram_service.try_send_chat_message(
                #     f"Zrealizowany webinar ID={webinar_id} nie ma podłączonej faktury. Coś jest nie tak? Do sprawdzenia.",
                #     TelegramChats.OTHER,
                # )
                continue

            # Find the first category with a Fakturownia category ID
            if not webinar.fakturownia_category:
                print("Skipping: webinar.fakturownia_category is not set.")
                continue

            category_id: str = webinar.fakturownia_category.fakturownia_id

            print("Using Fakturownia Category ID:", category_id)

            # Retrieve current invoice data from Fakturownia
            try:
                response = requests.get(
                    f"{settings.FAKTUROWNIA_API_URL}/invoices/{invoice_id}.json",
                    params={"api_token": settings.FAKTUROWNIA_API_KEY},
                    timeout=10,
                )
                response.raise_for_status()
                invoice_data = response.json()
            except requests.RequestException as e:
                print(f"Error fetching invoice data: {e}")
                continue

            # Check if the category ID is already set in Fakturownia
            if invoice_data.get("category_id"):
                print("Category ID already set in Fakturownia. No update needed.")
                continue

            # Prepare and send update to set the category ID in Fakturownia
            print("Updating Category ID in Fakturownia.")
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            data = {
                "api_token": settings.FAKTUROWNIA_API_KEY,
                "invoice": {"category_id": category_id},
            }

            try:
                update_response = requests.put(
                    f"{settings.FAKTUROWNIA_API_URL}/invoices/{invoice_id}.json",
                    headers=headers,
                    json=data,
                    timeout=10,
                )
                update_response.raise_for_status()
                print("Update successful:", update_response.json())
            except requests.RequestException as e:
                print(f"Error updating invoice: {e}")
