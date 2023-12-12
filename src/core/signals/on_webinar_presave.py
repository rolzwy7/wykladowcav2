"""
Webinar presave
"""

# flake8: noqa=E501
# pylint: disable=line-too-long

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

    if not kwargs.get("instance"):
        return

    webinar: Webinar = kwargs["instance"]

    # Remove special characters from titles
    for _ in ["\r", "\n", "\t"]:
        webinar.title_original = webinar.title_original.replace(_, "")
        webinar.title = webinar.title.replace(_, "")
        webinar.description = webinar.description.replace(_, "")

    # Remove multiple spaces from titles
    for _ in range(5):
        webinar.title_original = webinar.title_original.replace(" " * 2, " ")
        webinar.title = webinar.title.replace(" " * 2, " ")
        webinar.description = webinar.description.replace(" " * 2, " ")

    # Calculate webinar's slug
    if not webinar.slug:
        webinar.slug = f"{slugify(webinar.title)}-{randint(1_000, 99_999)}"

    # Remove <br /> tags from webinar's program
    for _ in ["<br />", "<br/>", "<br>"]:
        webinar.program = webinar.program.replace(_, "")

    # Generate markdown version
    webinar.program_markdown = markdownify(webinar.program)

    # Generate pretty version
    webinar.program_pretty = ProgramService(webinar.program_markdown).get_enriched()
