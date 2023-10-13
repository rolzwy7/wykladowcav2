# pylint: disable=global-variable-not-assigned
from django.core.management.base import BaseCommand

from core.models.tagging import TaggedEmailManager

PREFIX_MAP = {
    "KSIEGOWOSC": [
        "gk",
        "gksiegowosc",
        "gl.ksiegowosc",
        "gl.ksiegowy",
        "glksiegowa",
        "glksiegowosc",
        "ksiegowa",
        "ksiegowosc",
        "kwestura",
    ],
    "KADRY": [
        "kadrowa",
        "kadry",
    ],
}


class Command(BaseCommand):
    """Auto tag emails"""

    help = "Auto tag emails"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("Auto tag emails")

        manager = TaggedEmailManager()

        # Tag by prefix
        for tag, prefixes in PREFIX_MAP.items():
            for prefix in prefixes:
                print(f"\nTagging prefix `{prefix}` with tag `{tag}`")
                result = manager.collection.update_many(
                    {"prefix": prefix},
                    {"$addToSet": {"tags": {"$each": [tag]}}},
                )
                print("Matched:", result.matched_count)
                print("Modified:", result.modified_count)

        manager.close()
