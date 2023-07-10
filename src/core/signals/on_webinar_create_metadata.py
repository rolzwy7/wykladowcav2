from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Webinar, WebinarMetadata


@receiver(post_save, sender=Webinar, dispatch_uid="768af10938")
def on_webinar_create_metadata(sender, **kwargs):
    """Create webinar's metadata after save"""
    if kwargs.get("instance"):
        # Create metadata
        webinar: Webinar = kwargs["instance"]
        WebinarMetadata.objects.get_or_create(webinar=webinar)
