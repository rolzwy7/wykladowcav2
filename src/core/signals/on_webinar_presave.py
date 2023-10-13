from django.db.models.signals import pre_save
from django.dispatch import receiver
from markdownify import markdownify

from core.models import Webinar
from core.services import ProgramService
from core.utils.text import slugify


@receiver(pre_save, sender=Webinar, dispatch_uid="1f4ea25e80")
def on_webinar_presave(sender, **kwargs):
    """On Webinar Presave"""
    if kwargs.get("instance"):
        webinar: Webinar = kwargs["instance"]

        webinar.slug = slugify(webinar.title)

        webinar.title_original = webinar.title_original.replace("\r\n", "")
        webinar.title = webinar.title.replace("\r\n", "")
        webinar.description = webinar.description.replace("\r\n", "")

        webinar.title_original = webinar.title_original.replace("\n", "")
        webinar.title = webinar.title.replace("\n", "")
        webinar.description = webinar.description.replace("\n", "")

        webinar.program_markdown = markdownify(webinar.program)

        webinar.program_enchanted = ProgramService(
            webinar.program_markdown
        ).get_enriched()
