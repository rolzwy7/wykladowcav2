"""
Webinar presave
"""

# flake8: noqa=E501
# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=unused-variable
# pylint: disable=broad-exception-caught

from bs4 import BeautifulSoup
from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.models import WebinarAggregate


def get_first_level_li(html_content: str):
    """Get first level li tags"""
    soup = BeautifulSoup(html_content, "lxml")

    def is_first_level_li(tag):
        return tag.name == "li" and not any(tag.find_parents("li", recursive=False))

    tags = [f"<li>{tag.contents[0]}</li>\n" for tag in soup.find_all(is_first_level_li)]

    return "".join(tags[:10])


@receiver(pre_save, sender=WebinarAggregate, dispatch_uid="2f4ea25e81")
def on_aggregate_presave(sender, instance, **kwargs):
    """On Webinar Presave"""

    # if not kwargs.get("instance"):
    #     return

    aggregate: WebinarAggregate = instance

    if instance.pk:
        try:
            existing = WebinarAggregate.manager.get(pk=instance.pk)
            created = False
        except WebinarAggregate.DoesNotExist:
            created = True
    else:
        created = True

    # Generate program summary
    try:
        aggregate.program_short = get_first_level_li(aggregate.program)
    except Exception as e:
        aggregate.program_short = "Nie udało się wygenerować krótkiego programu"
