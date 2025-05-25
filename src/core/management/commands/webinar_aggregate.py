"""
This script updates invoice categories on Fakturownia for completed webinars.
"""

# flake8: noqa=E501
from django.core.management.base import BaseCommand

from core.libs.webinar_aggregate import (
    aggregate_refresh_categories,
    aggregate_update_closest_webinar_dt,
    aggregate_update_conflicts,
    aggregate_update_has_active_webinars,
    get_or_create_aggregate,
)
from core.models import Webinar, WebinarAggregate


class Command(BaseCommand):
    """Command"""

    help = "Command webinar_aggregate"

    def add_arguments(self, parser):
        # Additional arguments can be defined here if needed in the future
        pass

    def handle(self, *args, **options):
        """handle"""

        for webinar in Webinar.manager.all():
            print("Webinar:", webinar)
            if not webinar.grouping_token:
                continue
            get_or_create_aggregate(webinar)

        for aggregate in WebinarAggregate.manager.all():
            print("Aggregate:", aggregate)

            print("Refreshing categories for:", aggregate)
            aggregate_refresh_categories(aggregate)

            print("Update closest webinar:", aggregate)
            aggregate_update_closest_webinar_dt(aggregate)

            print("Update conflicts:", aggregate)
            aggregate_update_conflicts(aggregate)

            print("Update has active webinars:", aggregate)
            aggregate_update_has_active_webinars(aggregate)

            print("")
