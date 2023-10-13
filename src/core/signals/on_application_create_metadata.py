from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import WebinarApplication, WebinarApplicationMetadata


@receiver(post_save, sender=WebinarApplication, dispatch_uid="9da49bf72f")
def on_application_create_metadata(sender, **kwargs):
    """Create application's metadata after save"""
    if kwargs.get("instance"):
        application: WebinarApplication = kwargs["instance"]
        WebinarApplicationMetadata.objects.get_or_create(
            application=application
        )
