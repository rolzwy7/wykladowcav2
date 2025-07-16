"""
history_clean_diff
"""

# flake8: noqa=E501
# pylint: disable=line-too-long

#
# To use this command, save it in a file named `delete_unchanged_history.py`
# inside a `management/commands` directory of one of your Django apps.
#
# Example App Structure:
# myapp/
# ├── __init__.py
# ├── admin.py
# ├── apps.py
# ├── management/
# │   ├── __init__.py
# │   └── commands/
# │       ├── __init__.py
# │       └── delete_unchanged_history.py
# ├── models.py
# └── ...
#
# Usage from your project's root directory:
#
# 1. To see which records would be deleted without actually deleting them:
#    python manage.py delete_unchanged_history --model="myapp.MyModel" --dry-run
#
# 2. To perform the deletion:
#    python manage.py delete_unchanged_history --model="myapp.MyModel"
#

import itertools

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    """
    A Django management command to delete historical records where no changes were made
    compared to the previous history entry for the same object. This is optimized to
    avoid N+1 query problems and includes a --dry-run safety feature.
    """

    help = "Deletes historical records where no changes were made compared to the previous record."

    def add_arguments(self, parser):
        """Adds command-line arguments to the command."""
        parser.add_argument(
            "--model",
            type=str,
            help="Required. The model to process, in the format 'app_label.ModelName' (e.g., 'myapp.Book').",
            required=True,
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="If set, the command will only report which records would be deleted without actually deleting them.",
        )

    def handle(self, *args, **options):
        """The main logic of the command."""
        model_str = options["model"]
        is_dry_run = options["dry_run"]

        try:
            app_label, model_name = model_str.split(".")
            model = apps.get_model(app_label=app_label, model_name=model_name)
        except (ValueError, LookupError):
            self.stderr.write(
                self.style.ERROR(
                    f"Error: Model '{model_str}' not found. Please use the format 'app_label.ModelName'."
                )
            )
            return

        # Check if the model has a history attribute
        if not hasattr(model, "history"):
            self.stderr.write(
                self.style.ERROR(
                    f"Error: Model '{model_str}' does not appear to have a history manager. Is it registered with django-simple-history?"
                )
            )
            return

        history_model = model.history.model
        pk_name = model._meta.pk.name

        self.stdout.write(f"Processing historical records for {model_str}...")
        if is_dry_run:
            self.stdout.write(
                self.style.WARNING("--- DRY RUN MODE --- No records will be deleted.")
            )

        # Fetch all update records once, ordered by object ID and then by date
        # This allows us to group them efficiently in memory
        history_queryset = history_model.objects.filter(history_type="~").order_by(
            pk_name, "history_date"
        )

        records_to_delete = []

        # Group records by the primary key of the original model
        for _, group in itertools.groupby(
            history_queryset, key=lambda x: getattr(x, pk_name)
        ):
            # The group is an iterator, convert to list to access previous records
            records = list(group)
            for i in range(1, len(records)):
                current_record = records[i]
                prev_record = records[i - 1]

                # Use the built-in diffing method from django-simple-history
                diff = current_record.diff_against(prev_record)

                # If there are no changes, mark the record for deletion
                if not diff.changes:
                    records_to_delete.append(current_record.history_id)
                    self.stdout.write(
                        f"Found unchanged record for {model_name} object (PK: {getattr(current_record, pk_name)}) "
                        f"at {current_record.history_date} (History ID: {current_record.history_id})"
                    )

        deleted_count = len(records_to_delete)

        if not records_to_delete:
            self.stdout.write(
                self.style.SUCCESS(
                    "Completed. No unchanged history records found to delete."
                )
            )
            return

        if not is_dry_run:
            try:
                # Perform the deletion in a single, atomic transaction
                with transaction.atomic():
                    history_model.objects.filter(
                        history_id__in=records_to_delete
                    ).delete()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\nSuccessfully deleted {deleted_count} unchanged history records."
                    )
                )
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f"\nAn error occurred during deletion: {e}")
                )
                self.stderr.write(
                    self.style.ERROR(
                        "The transaction has been rolled back. No records were deleted."
                    )
                )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nDry run complete. Would have deleted {deleted_count} unchanged history records."
                )
            )
