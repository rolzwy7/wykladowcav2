"""
Controller for generating og:image for webinar
"""

# flake8: noqa=E501
# pylint: disable=line-too-long

from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import date as _date
from django.utils.timezone import get_default_timezone
from PIL import Image, ImageDraw

from core.models import Webinar, WebinarAggregate
from core.utils.pillow import draw_multiline_text, load_font

BASE_DIR = settings.BASE_DIR
ASSETS_DIR: Path = BASE_DIR.parent / "core" / "assets"
MEDIA_DIR: Path = BASE_DIR.parent / "public" / "media"


def aggregate_ogimage_page(request: HttpRequest, grouping_token: str):
    """View for generating og:image for webinar"""

    to_tz = get_default_timezone()
    aggregate = get_object_or_404(WebinarAggregate, grouping_token=grouping_token)

    # nearest_webinar = (
    #     Webinar.manager.get_active_webinars()
    #     .filter(id__in=[_.id for _ in aggregate.webinars.all()])
    #     .order_by("date")
    #     .first()
    # )

    width, height = 940, 788

    if aggregate.is_anonymized:
        return HttpResponse(status=404)

    # if nearest_webinar:
    #     nearest_webinar_date = nearest_webinar.date.astimezone(to_tz)

    base_layer = Image.open(
        ASSETS_DIR / "webinar_ogimage" / "og_image_agg_base.png"
    ).convert("RGBA")

    layer = Image.new("RGBA", (width, height), (255, 255, 255, 0))  # type: ignore

    font_24m = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Medium.ttf"), 24)
    font_30b = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Bold.ttf"), 30)
    font_35b = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Bold.ttf"), 35)
    font_20ri = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Italic.ttf"), 20)

    draw = ImageDraw.Draw(layer)

    draw.text((75, 125), "Webinar", font=font_30b, fill=(0, 0, 0, 255))

    if len(aggregate.title) < 140:
        draw_multiline_text(
            draw, font_35b, aggregate.title, (75, 160), 800, fill=(117, 79, 254, 255)
        )
    else:
        draw_multiline_text(
            draw, font_30b, aggregate.title, (75, 160), 800, fill=(117, 79, 254, 255)
        )

    draw.text(
        (75, 300), aggregate.lecturer.fullname, font=font_30b, fill=(0, 0, 0, 255)
    )

    if aggregate.lecturer.very_short_biography:
        draw_multiline_text(
            draw,
            font_20ri,
            aggregate.lecturer.very_short_biography,
            (75, 340),
            350,
            fill=(0, 0, 0, 255),
        )

    # if nearest_webinar:
    #     draw.text(
    #         (150, 465),
    #         _date(nearest_webinar_date, "l").upper(),
    #         font=font_24m,
    #         fill=(0, 0, 0, 255),
    #     )
    #     draw.text(
    #         (150, 495),
    #         _date(nearest_webinar_date, "j E Y").upper(),
    #         font=font_24m,
    #         fill=(0, 0, 0, 255),
    #     )

    #     draw.text((150, 540), "GODZINA", font=font_24m, fill=(0, 0, 0, 255))
    #     draw.text(
    #         (150, 570),
    #         _date(nearest_webinar_date, "H:i"),
    #         font=font_24m,
    #         fill=(0, 0, 0, 255),
    #     )

    out = Image.alpha_composite(base_layer, layer)

    if aggregate.lecturer.avatar:
        lecturer_im = Image.open(
            MEDIA_DIR
            / "uploads"
            / "lecturers"
            / f"{aggregate.lecturer.slug}_500x500.webp"
        ).convert("RGBA")
        out.paste(lecturer_im.resize((350, 350)), (460, 340))

    # Create byte buffer
    bytes_io = BytesIO()

    # Save PDF bytes to buffer
    out.save(bytes_io, format="PNG", save_all=True)

    # Get and return PDF bytes
    return HttpResponse(bytes_io.getvalue(), content_type="image/png")
