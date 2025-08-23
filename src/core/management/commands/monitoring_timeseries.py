"""dev_command"""

# flake8: noqa=E501
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from core.libs.mongo import timeseries
from core.libs.mongo.db import get_dwpldbv3_connection
from core.models import (
    BlacklistedDomain,
    BlacklistedEmail,
    BlacklistedEmailTemporary,
    BlacklistedPhrase,
    BlacklistedPrefix,
)


class Command(BaseCommand):
    """dev_command"""

    help = "Monitoring timeseries"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        client, db = get_dwpldbv3_connection()
        collection = db["wykladowcav2_timeseries"]

        # Monitor blacklists
        count_blck_domain = BlacklistedDomain.manager.count()
        timeseries.insert_event(
            collection,
            "blacklist_domain",
            "MailingSystem",
            {"count": count_blck_domain},
            check_for_change=True,
        )

        count_blck_email = BlacklistedEmail.manager.count()
        timeseries.insert_event(
            collection,
            "blacklist_email",
            "MailingSystem",
            {"count": count_blck_email},
            check_for_change=True,
        )

        count_blck_temp_email = BlacklistedEmailTemporary.manager.count()
        timeseries.insert_event(
            collection,
            "blacklist_temp_email",
            "MailingSystem",
            {"count": count_blck_temp_email},
            check_for_change=True,
        )

        count_blck_temp_email_active = BlacklistedEmailTemporary.manager.filter(
            expires_at__gt=now()
        ).count()
        timeseries.insert_event(
            collection,
            "blacklist_temp_email_active",
            "MailingSystem",
            {"count": count_blck_temp_email_active},
            check_for_change=True,
        )

        count_blck_phrase = BlacklistedPhrase.manager.count()
        timeseries.insert_event(
            collection,
            "blacklist_phrase",
            "MailingSystem",
            {"count": count_blck_phrase},
            check_for_change=True,
        )

        count_blck_prefix = BlacklistedPrefix.manager.count()
        timeseries.insert_event(
            collection,
            "blacklist_prefix",
            "MailingSystem",
            {"count": count_blck_prefix},
            check_for_change=True,
        )

        client.close()
