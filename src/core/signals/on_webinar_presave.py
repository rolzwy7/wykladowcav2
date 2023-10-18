from random import randint

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

        if not webinar.slug:
            webinar.slug = f"{slugify(webinar.title)}-{randint(1_000, 99_999)}"

        for _ in ["\r\n", "\n"]:
            webinar.title_original = webinar.title_original.replace(_, "")
            webinar.title = webinar.title.replace(_, "")
            webinar.description = webinar.description.replace(_, "")

        webinar.program_markdown = markdownify(webinar.program)

        webinar.program_enchanted = ProgramService(
            webinar.program_markdown
        ).get_enriched()
