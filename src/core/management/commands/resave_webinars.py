"""
This script updates invoice categories on Fakturownia for completed webinars.
"""

# flake8: noqa=E501
from django.core.management.base import BaseCommand

from core.models import Webinar


class Command(BaseCommand):
    """Command"""

    help = "Command resave webinars"

    def add_arguments(self, parser):
        # Additional arguments can be defined here if needed in the future
        pass

    def handle(self, *args, **options):
        """handle"""

        webinars: list[Webinar] = [_ for _ in Webinar.manager.all()]

        while webinars:
            webinar = webinars.pop()
            print("[*] Re-saving:", webinar)
            webinar.save()

        print("[+] Done.")
