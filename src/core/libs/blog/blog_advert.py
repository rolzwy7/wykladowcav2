"""Blog advert image"""

# flake8: noqa=E501

from django.conf import settings
from django.urls import reverse

from core.models import WebinarAggregate


def get_blogpost_advert_img_tag(aggregate: WebinarAggregate):
    """get_blogpost_advert_img_tag"""

    grouping_token = aggregate.grouping_token

    alt = aggregate.title
    aggregate_url = settings.BASE_URL + reverse(
        "core:webinar_aggregate_page",
        kwargs={"slug": aggregate.slug},
    )
    src = settings.BASE_URL + reverse(
        "core:webinar_aggregate_advert_banner",
        kwargs={"grouping_token": grouping_token, "resolution": "1940x700"},
    )

    srcset = ", ".join(
        [
            settings.BASE_URL
            + reverse(
                "core:webinar_aggregate_advert_banner",
                kwargs={"grouping_token": grouping_token, "resolution": resolution},
            )
            + " "
            + w_units
            for resolution, w_units in [
                ("768x277", "768w"),
                ("800x289", "800w"),
                ("1024x369", "1024w"),
                ("1536x554", "1536w"),
                ("1940x700", "1940w"),
            ]
        ]
    )

    return " ".join(
        [
            f'<p><a href="{aggregate_url}">',
            '<img fetchpriority="high" decoding="async" style="width: 100%; height: auto;"',
            f'src="{src}" alt="{alt}" width="1940" height="700"',
            f'srcset="{srcset}" sizes="(max-width: 1940px) 100vw, 1940px">',
            "</a></p>",
        ]
    )
