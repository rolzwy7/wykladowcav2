from django.db.models.fields.files import ImageFieldFile
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Lecturer
from core.utils.image import create_thumbnails_for_lecturer


@receiver(post_save, sender=Lecturer, dispatch_uid="47db377000")
def on_lecturer_save_make_thumbnails(sender, **kwargs):
    if not kwargs.get("instance"):
        return

    instance: Lecturer = kwargs["instance"]
    avatar: ImageFieldFile = instance.avatar

    if avatar:
        create_thumbnails_for_lecturer(
            str(avatar), avatar.instance  # type: ignore
        )
