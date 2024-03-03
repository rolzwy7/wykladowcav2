"""Core Apps"""

# pylint: disable=import-outside-toplevel
# pylint: disable=unused-import


from django.apps import AppConfig

from wykladowcapl import settings


class CoreConfig(AppConfig):
    """Core config"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    verbose_name = "Główna aplikacja"

    def ready(self):
        # Load all signals implicitly
        from . import signals  # noqa
