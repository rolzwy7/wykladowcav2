# pylint: disable=global-variable-not-assigned

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Auto tag emails"""

    help = "Auto tag emails"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("Auto tag emails")  # TODO: Auto tag emails
