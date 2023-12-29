"""
Webinar presave
"""

# flake8: noqa=E501
# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=unused-variable
# pylint: disable=broad-exception-caught

from random import randint

from bs4 import BeautifulSoup
from django.db.models.signals import pre_save
from django.dispatch import receiver
from markdownify import markdownify

from core.models import Webinar
from core.services import ProgramService
from core.utils.text import slugify


def get_first_level_li(html_content: str):
    """Get first level li tags"""
    soup = BeautifulSoup(html_content, "lxml")

    def is_first_level_li(tag):
        return tag.name == "li" and not any(tag.find_parents("li", recursive=False))

    tags = [f"<li>{tag.contents[0]}</li>\n" for tag in soup.find_all(is_first_level_li)]

    return "".join(tags[:10])


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

    if not webinar.program_short:
        try:
            # Generate program summary
            webinar.program_short = get_first_level_li(webinar.program)
        except Exception as e:
            webinar.program_short = "Nie udało się wygenerować krótkiego programu"
