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

from core.models import Lecturer
from core.utils.pillow import draw_multiline_text, load_font

BASE_DIR = settings.BASE_DIR
ASSETS_DIR: Path = BASE_DIR.parent / "core" / "assets"
MEDIA_DIR: Path = BASE_DIR.parent / "public" / "media"


def lecturer_ogimage_page(request: HttpRequest, slug: str):
    """View for generating og:image for webinar"""

    lecturer = get_object_or_404(Lecturer, slug=slug)
    width, height = 940, 788

    base_layer = Image.open(
        ASSETS_DIR / "webinar_ogimage" / "og_image_lecturer_base.png"
    ).convert("RGBA")

    layer = Image.new("RGBA", (width, height), (255, 255, 255, 0))  # type: ignore

    font_24m = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Medium.ttf"), 24)
    font_30b = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Bold.ttf"), 30)
    font_25b = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Bold.ttf"), 25)
    font_35b = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Bold.ttf"), 35)
    font_20ri = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Italic.ttf"), 20)

    draw = ImageDraw.Draw(layer)

    draw.text((75, 300), lecturer.fullname, font=font_30b, fill=(0, 0, 0, 255))

    if lecturer.very_short_biography:
        draw_multiline_text(
            draw,
            font_20ri,
            lecturer.very_short_biography,
            (75, 340),
            350,
            fill=(0, 0, 0, 255),
        )

    out = Image.alpha_composite(base_layer, layer)

    if lecturer.avatar:
        lecturer_im = Image.open(
            MEDIA_DIR / "uploads" / "lecturers" / f"{lecturer.slug}_500x500.webp"
        ).convert("RGBA")
        out.paste(lecturer_im.resize((350, 350)), (460, 340))

    # Create byte buffer
    bytes_io = BytesIO()

    # Save PDF bytes to buffer
    out.save(bytes_io, format="PNG", save_all=True)

    # Get and return PDF bytes
    return HttpResponse(bytes_io.getvalue(), content_type="image/png")
