from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    verbose_name = "Główna aplikacja"

    def ready(self):
        # Load all signals implicitly
        from . import signals  # noqa
