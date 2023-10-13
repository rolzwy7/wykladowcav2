from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import WebinarParticipant, WebinarParticipantMetadata


@receiver(post_save, sender=WebinarParticipant, dispatch_uid="729f5f49dd")
def on_webinar_participanta_create_metadata(sender, **kwargs):
    """Create webinar's metadata after save"""
    if kwargs.get("instance"):
        participant: WebinarParticipant = kwargs["instance"]
        WebinarParticipantMetadata.objects.get_or_create(
            participant=participant
        )
