"""mailing/management/commands/reset_campaign_errors.py"""

# flake8: noqa=E501

from django.core.management.base import BaseCommand
from django.db.models import Q

# Assuming your MailingCampaign model is in an app named 'core'
# Please adjust the import path if your model is located elsewhere.
from core.models import MailingCampaign


class Command(BaseCommand):
    """
    A Django management command to reset specific error flags on MailingCampaign models.
    """

    help = (
        "Resets error flags (any_error_occured, smtp_server_disconnected, "
        "connection_refused, smtp_recipients_refused) to False for all "
        "MailingCampaigns where at least one of these flags is True."
    )

    def handle(self, *args, **options):
        """
        The main logic for the command.

        This method finds all MailingCampaign objects that have one or more
        of the specified error flags set to True and resets them to False
        in a single, efficient database query.
        """
        self.stdout.write("Starting to reset campaign error flags...")

        # Define the fields to be reset
        error_fields = [
            "any_error_occured",
            "smtp_server_disconnected",
            "connection_refused",
            "smtp_recipients_refused",
        ]

        # Build a query to find campaigns with at least one error flag set.
        # This makes the update more efficient by not touching campaigns
        # that have no errors.
        query_filter = Q()
        for field in error_fields:
            query_filter |= Q(**{field: True})

        campaigns_with_errors = MailingCampaign.manager.filter(query_filter)

        # Get the count before updating
        update_count = campaigns_with_errors.count()

        if update_count == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    "No campaigns with active error flags found. Nothing to do."
                )
            )
            return

        # Prepare the data for the update operation
        update_data = {field: False for field in error_fields}

        # Perform the bulk update for efficiency.
        # The update() method runs a single SQL query.
        updated_rows = campaigns_with_errors.update(**update_data)

        # Output a success message to the console
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully reset error flags for {updated_rows} mailing campaigns."
            )
        )
