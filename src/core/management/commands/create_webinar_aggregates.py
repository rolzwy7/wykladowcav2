"""
Mailing sending procedure
"""

# flake8: noqa:E501
# pylint: disable=global-variable-not-assigned
# pylint: disable=broad-exception-caught
# pylint: disable=unused-variable
# pylint: disable=invalid-name

from django.core.management.base import BaseCommand

from core.models import Webinar, WebinarAggregate


class Command(BaseCommand):
    """Create webinar aggregates"""

    help = "Create webinar aggregates"

    def add_arguments(self, parser): ...

    def handle(self, *args, **options):
        """handle"""

        for _webinar in Webinar.manager.all():
            webinar: Webinar = _webinar

            aggregate_exists = WebinarAggregate.manager.filter(
                grouping_token=webinar.grouping_token
            ).exists()

            if aggregate_exists:
                print(f"[*] Aggregate for {webinar.grouping_token} already exists")
                continue

            webinar_aggregate = WebinarAggregate(
                grouping_token=webinar.grouping_token, slug=webinar.slug
            )

            webinar_aggregate.save()

            print("[+] Created aggregated for:", webinar.grouping_token)
