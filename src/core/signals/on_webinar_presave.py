"""
Webinar presave
"""

# flake8: noqa=E501
# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=unused-variable
# pylint: disable=broad-exception-caught

from random import choice, randint, shuffle
from string import ascii_uppercase, digits
from typing import Optional

from bs4 import BeautifulSoup
from django.db.models.signals import pre_save
from django.dispatch import receiver
from markdownify import markdownify

from core.libs.html_operations.program import program_normalize, program_remarkdownify
from core.models import Webinar, WebinarAggregate
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
def on_webinar_presave(sender, instance, **kwargs):
    """On Webinar Presave"""

    # if not kwargs.get("instance"):
    #     return

    webinar: Webinar = instance

    if instance.pk:
        try:
            existing = Webinar.manager.get(pk=instance.pk)
            created = False
        except Webinar.DoesNotExist:
            created = True
    else:
        created = True

    # Generate grouping token if doesn't exist
    if not webinar.grouping_token:
        random_base = list(f"{ascii_uppercase}{digits}")
        shuffle(random_base)

        for _ in range(1_000):
            code_candid = "".join([choice(random_base) for _ in range(8)])
            if Webinar.manager.filter(grouping_token=code_candid).exists():
                continue
            webinar.grouping_token = code_candid
            break

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

    # Override grouping token with existing aggragate if created
    if created:
        webinar_core_slug = "-".join(webinar.slug.split("-")[:-1])
        qs_conflict = WebinarAggregate.manager.filter(slug=webinar_core_slug)
        slug_conflict = qs_conflict.exists()
        if slug_conflict:
            already_existing_aggregate: WebinarAggregate = qs_conflict.first()  # type: ignore
            webinar.grouping_token = already_existing_aggregate.grouping_token

    # Remove <br /> tags from webinar's program
    for _ in ["<br />", "<br/>", "<br>"]:
        webinar.program = webinar.program.replace(_, "")

    # Generate markdown version
    webinar.program_markdown = markdownify(webinar.program)

    # Generate pretty version
    webinar.program_pretty = ProgramService(webinar.program_markdown).get_enriched()

    # Normalize webinar program
    webinar.program = program_normalize(program_remarkdownify(webinar.program))

    # Generate program summary
    try:
        webinar.program_short = get_first_level_li(webinar.program)
    except Exception as e:
        webinar.program_short = "Nie udało się wygenerować krótkiego programu"
