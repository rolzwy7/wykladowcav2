"""
Mailing sending procedure
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Mailing subject TEST A/B"""

    help = "Mailing subject TEST A/B"

    def add_arguments(self, parser): ...

    def handle(self, *args, **options):
        """handle"""

        ...
