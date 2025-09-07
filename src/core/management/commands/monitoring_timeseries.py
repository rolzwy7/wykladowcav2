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

        #
        # Monitor blacklists
        #

        client, db = get_dwpldbv3_connection()
        timeseries_collection = db["wykladowcav2_timeseries"]

        # Monitor blacklists
        count_blck_domain = BlacklistedDomain.manager.count()
        timeseries.insert_event(
            timeseries_collection,
            "blacklist_domain",
            "MailingSystem",
            {"count": count_blck_domain},
            check_for_change=True,
        )

        count_blck_email = BlacklistedEmail.manager.count()
        timeseries.insert_event(
            timeseries_collection,
            "blacklist_email",
            "MailingSystem",
            {"count": count_blck_email},
            check_for_change=True,
        )

        count_blck_temp_email = BlacklistedEmailTemporary.manager.count()
        timeseries.insert_event(
            timeseries_collection,
            "blacklist_temp_email",
            "MailingSystem",
            {"count": count_blck_temp_email},
            check_for_change=True,
        )

        count_blck_temp_email_active = BlacklistedEmailTemporary.manager.filter(
            expires_at__gt=now()
        ).count()
        timeseries.insert_event(
            timeseries_collection,
            "blacklist_temp_email_active",
            "MailingSystem",
            {"count": count_blck_temp_email_active},
            check_for_change=True,
        )

        count_blck_phrase = BlacklistedPhrase.manager.count()
        timeseries.insert_event(
            timeseries_collection,
            "blacklist_phrase",
            "MailingSystem",
            {"count": count_blck_phrase},
            check_for_change=True,
        )

        count_blck_prefix = BlacklistedPrefix.manager.count()
        timeseries.insert_event(
            timeseries_collection,
            "blacklist_prefix",
            "MailingSystem",
            {"count": count_blck_prefix},
            check_for_change=True,
        )

        #
        # Monitor verify
        #

        verify_collection = db["email_verify_valid_emails"]
        verify_count = verify_collection.estimated_document_count()
        timeseries.insert_event(
            timeseries_collection,
            "valid_emails",
            "DlpVerify",
            {"count": verify_count},
            check_for_change=True,
        )

        #
        # Monitor regon
        #

        regon_queue_collection = db["regon_queue"]
        regon_queue_count = regon_queue_collection.estimated_document_count()
        timeseries.insert_event(
            timeseries_collection,
            "regon_queue",
            "DlpRegon",
            {"count": regon_queue_count},
            check_for_change=True,
        )

        regon_ceidg_collection = db["regon_ceidg"]
        regon_ceidg_count = regon_ceidg_collection.estimated_document_count()
        timeseries.insert_event(
            timeseries_collection,
            "regon_ceidg",
            "DlpRegon",
            {"count": regon_ceidg_count},
            check_for_change=True,
        )

        regon_prawna_collection = db["regon_prawna"]
        regon_prawna_count = regon_prawna_collection.estimated_document_count()
        timeseries.insert_event(
            timeseries_collection,
            "regon_prawna",
            "DlpRegon",
            {"count": regon_prawna_count},
            check_for_change=True,
        )

        regon_rolnicza_collection = db["regon_rolnicza"]
        regon_rolnicza_count = regon_rolnicza_collection.estimated_document_count()
        timeseries.insert_event(
            timeseries_collection,
            "regon_rolnicza",
            "DlpRegon",
            {"count": regon_rolnicza_count},
            check_for_change=True,
        )

        regon_pozostala_collection = db["regon_pozostala"]
        regon_pozostala_count = regon_pozostala_collection.estimated_document_count()
        timeseries.insert_event(
            timeseries_collection,
            "regon_pozostala",
            "DlpRegon",
            {"count": regon_pozostala_count},
            check_for_change=True,
        )

        #
        # Monitor scraper
        #

        scraper_queue_static_collection = db["scraper_queue_static"]
        scraper_queue_static_count = (
            scraper_queue_static_collection.estimated_document_count()
        )
        timeseries.insert_event(
            timeseries_collection,
            "regon_pozostala",
            "DlpRegon",
            {"count": scraper_queue_static_count},
            check_for_change=True,
        )

        scraper_html_files_collection = db["scraper_html_files"]
        scraper_html_files_count = (
            scraper_html_files_collection.estimated_document_count()
        )
        timeseries.insert_event(
            timeseries_collection,
            "regon_pozostala",
            "DlpRegon",
            {"count": scraper_html_files_count},
            check_for_change=True,
        )

        scraper_found_nips_collection = db["scraper_found_nips"]
        scraper_found_nips_count = (
            scraper_found_nips_collection.estimated_document_count()
        )
        timeseries.insert_event(
            timeseries_collection,
            "regon_pozostala",
            "DlpRegon",
            {"count": scraper_found_nips_count},
            check_for_change=True,
        )

        scraper_found_emails_collection = db["scraper_found_emails"]
        scraper_found_emails_count = (
            scraper_found_emails_collection.estimated_document_count()
        )
        timeseries.insert_event(
            timeseries_collection,
            "regon_pozostala",
            "DlpRegon",
            {"count": scraper_found_emails_count},
            check_for_change=True,
        )

        scraper_best_privacy_policy_urls_collection = db[
            "scraper_best_privacy_policy_urls"
        ]
        scraper_best_privacy_policy_urls_count = (
            scraper_best_privacy_policy_urls_collection.estimated_document_count()
        )
        timeseries.insert_event(
            timeseries_collection,
            "regon_pozostala",
            "DlpRegon",
            {"count": scraper_best_privacy_policy_urls_count},
            check_for_change=True,
        )

        scraper_best_contact_urls_collection = db["scraper_best_contact_urls"]
        scraper_best_contact_urls_count = (
            scraper_best_contact_urls_collection.estimated_document_count()
        )
        timeseries.insert_event(
            timeseries_collection,
            "regon_pozostala",
            "DlpRegon",
            {"count": scraper_best_contact_urls_count},
            check_for_change=True,
        )

        wizytowki_core_method_collection = db["wizytowki_core_method"]
        wizytowki_core_method_count = (
            wizytowki_core_method_collection.estimated_document_count()
        )
        timeseries.insert_event(
            timeseries_collection,
            "regon_pozostala",
            "DlpRegon",
            {"count": wizytowki_core_method_count},
            check_for_change=True,
        )

        #
        #
        # Close mongo connection
        client.close()
