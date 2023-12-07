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

from core.models import Webinar
from core.utils.pillow import draw_multiline_text, load_font

BASE_DIR = settings.BASE_DIR
ASSETS_DIR: Path = BASE_DIR.parent / "core" / "assets"
MEDIA_DIR: Path = BASE_DIR.parent / "public" / "media"


def webinar_ogimage_page(request: HttpRequest, pk: int):
    """View for generating og:image for webinar"""

    webinar = get_object_or_404(Webinar, pk=pk)
    width, height = 940, 788

    to_tz = get_default_timezone()
    date = webinar.date.astimezone(to_tz)

    base_layer = Image.open(
        ASSETS_DIR / "webinar_ogimage" / "og_image_base.png"
    ).convert("RGBA")

    layer = Image.new("RGBA", (width, height), (255, 255, 255, 0))

    font_24m = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Medium.ttf"), 24)
    font_30b = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Bold.ttf"), 30)
    font_35b = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Bold.ttf"), 35)
    font_20ri = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Italic.ttf"), 20)

    draw = ImageDraw.Draw(layer)

    draw.text((75, 125), "Webinar", font=font_30b, fill=(0, 0, 0, 255))

    if len(webinar.title) < 140:
        draw_multiline_text(
            draw, font_35b, webinar.title, (75, 160), 800, fill=(117, 79, 254, 255)
        )
    else:
        draw_multiline_text(
            draw, font_30b, webinar.title, (75, 160), 800, fill=(117, 79, 254, 255)
        )

    draw.text((75, 300), webinar.lecturer.fullname, font=font_30b, fill=(0, 0, 0, 255))

    if webinar.lecturer.very_short_biography:
        draw_multiline_text(
            draw,
            font_20ri,
            webinar.lecturer.very_short_biography,
            (75, 340),
            350,
            fill=(0, 0, 0, 255),
        )

    draw.text((150, 465), _date(date, "l").upper(), font=font_24m, fill=(0, 0, 0, 255))
    draw.text(
        (150, 495),
        _date(date, "j E Y").upper(),
        font=font_24m,
        fill=(0, 0, 0, 255),
    )

    draw.text((150, 540), "GODZINA", font=font_24m, fill=(0, 0, 0, 255))
    draw.text((150, 570), _date(date, "H:i"), font=font_24m, fill=(0, 0, 0, 255))

    out = Image.alpha_composite(base_layer, layer)

    if webinar.lecturer.avatar:
        lecturer_im = Image.open(
            MEDIA_DIR
            / "uploads"
            / "lecturers"
            / f"{webinar.lecturer.slug}_500x500.webp"
        ).convert("RGBA")
        out.paste(lecturer_im.resize((350, 350)), (460, 340))

    # Create byte buffer
    bytes_io = BytesIO()

    # Save PDF bytes to buffer
    out.save(bytes_io, format="PNG", save_all=True)

    # Get and return PDF bytes
    return HttpResponse(bytes_io.getvalue(), content_type="image/png")
