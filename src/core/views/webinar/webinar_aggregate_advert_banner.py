"""webinar_aggregate_page"""

# flake8: noqa=E501

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
CORE_STATIC_DIR: Path = BASE_DIR.parent / "core" / "static"
MEDIA_DIR: Path = BASE_DIR.parent / "public" / "media"


def webinar_aggregate_advert_banner(request, grouping_token: str):
    """webinar_aggregate_advert_banner"""

    aggregate = get_object_or_404(WebinarAggregate, grouping_token=grouping_token)

    width, height = 1940, 700
    primary_color = (117, 79, 254)

    # base_layer = Image.open(
    #     ASSETS_DIR / "aggregate_blogpost_banner" / "aggregate_blogpost_banner_base.png"
    # ).convert("RGBA")

    # "media", "logos", "wykladowcapl", "logo.svg"

    font_24m = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Medium.ttf"), 24)
    font_30b = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Bold.ttf"), 30)
    font_35b = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Bold.ttf"), 35)
    font_20ri = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Italic.ttf"), 20)

    layer1 = Image.new("RGBA", (width, height), (255, 255, 255, 255))  # type: ignore
    layer2 = Image.new("RGBA", (width, height), (255, 255, 255, 0))  # type: ignore

    # --- Add two nested circles on the right ---
    # Create a drawing context on the first layer
    draw = ImageDraw.Draw(layer1)

    # This is drawn first, so it appears behind the other elements.
    draw.rectangle(
        (0, 85, width, 550),
        fill=(*primary_color, 255),
    )

    # --- Outer Circle ---
    # Define the bounding box for the outer circle
    outer_circle_diameter = 550
    outer_circle_x0 = width - outer_circle_diameter - 100  # 100px from the right edge
    outer_circle_y0 = (height - outer_circle_diameter) / 2 + 25
    outer_circle_x1 = outer_circle_x0 + outer_circle_diameter
    outer_circle_y1 = outer_circle_y0 + outer_circle_diameter

    # Draw a light gray, fully opaque ellipse (circle)
    draw.ellipse(
        (outer_circle_x0, outer_circle_y0, outer_circle_x1, outer_circle_y1),
        fill=(255, 255, 255, 255),
    )

    # --- Inner Circle ---
    # Define the bounding box for the inner circle
    inner_circle_diameter = 500  # Slightly smaller
    # Calculate offset to center the inner circle within the outer one
    offset = (outer_circle_diameter - inner_circle_diameter) / 2
    inner_circle_x0 = outer_circle_x0 + offset
    inner_circle_y0 = outer_circle_y0 + offset
    inner_circle_x1 = inner_circle_x0 + inner_circle_diameter
    inner_circle_y1 = inner_circle_y0 + inner_circle_diameter

    # --- STEP 1: LOAD THE IMAGE TO PLACE INSIDE THE CIRCLE ---
    img_to_mask = Image.open(
        MEDIA_DIR / "uploads" / "lecturers" / f"{aggregate.lecturer.slug}_500x500.webp"
    ).convert("RGBA")

    # # Resize the image to fit the circle's dimensions
    img_to_mask = img_to_mask.resize((inner_circle_diameter, inner_circle_diameter))

    # layer2.paste(img_to_mask, (460, 10))

    # --- STEP 2: CREATE THE CIRCULAR MASK ---
    # Create a new black image ('L' mode for grayscale) for the mask
    mask = Image.new("L", (inner_circle_diameter, inner_circle_diameter), 0)
    # Create a draw object to draw on the mask
    mask_draw = ImageDraw.Draw(mask)
    # Draw a white, filled circle on the black mask.
    # The white area is what will be kept from the original image.
    mask_draw.ellipse((0, 0, inner_circle_diameter, inner_circle_diameter), fill=255)

    # Draw a white, fully opaque ellipse (circle) inside the other one
    draw.ellipse(
        (inner_circle_x0, inner_circle_y0, inner_circle_x1, inner_circle_y1),
        fill=(255, 255, 255, 255),
    )

    # --- STEP 3: PASTE THE MASKED IMAGE ONTO THE BANNER ---
    # The 'mask' argument ensures that only the circular part of the image is pasted
    layer1.paste(img_to_mask, (int(inner_circle_x0), int(inner_circle_y0)), mask)

    # --- Rounded Rectangle ---
    # Define bounding box and radius for the rectangle
    rect_x0 = 75  # 100px from the left edge
    rect_height = 100
    rect_y0 = height - rect_height - 30  # 60px from the bottom edge
    rect_width = 400
    rect_x1 = rect_x0 + rect_width
    rect_y1 = rect_y0 + rect_height
    radius = 75

    # Draw a white, fully opaque rounded rectangle with a gray border
    draw.rounded_rectangle(
        (rect_x0, rect_y0, rect_x1, rect_y1),
        radius=radius,
        fill=(*primary_color, 255),
        outline=(255, 255, 255, 255),
        width=4,
    )

    font_text_sprawdz = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Bold.ttf"), 40)
    draw.text(
        (rect_x0 + rect_width / 2 - 120, rect_y0 + 22),
        "SPRAWDŹ >",
        font=font_text_sprawdz,
        fill=(255, 255, 255, 255),
    )

    font_szkolenie_online = load_font(
        str(ASSETS_DIR / "fonts" / "Montserrat-Bold.ttf"), 32
    )
    draw.text(
        (75, 24),
        "SZKOLENIE ONLINE",
        font=font_szkolenie_online,
        fill=(24, 17, 60, 255),
    )

    logo_im = Image.open(
        CORE_STATIC_DIR / "media" / "logos" / "wykladowcapl" / "logo.png"
    ).convert("RGBA")
    layer2.paste(logo_im, (1520, 10))

    # draw.rectangle(
    #     (75, 450, 400, 10),
    #     fill=(255, 255, 255, 255),
    # )

    # Calendar
    calendar_position = (75, 475)
    calendar_im = Image.open(
        ASSETS_DIR / "aggregate_blogpost_banner" / "calendar-days.png"
    ).convert("RGBA")
    data = list(calendar_im.getdata())
    new_data = []
    for pixel in data:
        if pixel[3] != 0:
            new_data.append((255, 255, 255, pixel[3]))
        else:
            new_data.append(pixel)  # Keep original
    calendar_im.putdata(new_data)
    layer2.paste(calendar_im.resize((48, 48)), calendar_position)

    font_calendar_date = load_font(
        str(ASSETS_DIR / "fonts" / "Montserrat-Medium.ttf"), 32
    )
    draw.text(
        (calendar_position[0] + 65, calendar_position[1] + 5),
        _date(aggregate.closest_webinar_dt, "d.m.Y"),
        font=font_calendar_date,
        fill=(255, 255, 255, 255),
    )

    # Clock
    clock_position = (350, 475)
    clock_im = Image.open(
        ASSETS_DIR / "aggregate_blogpost_banner" / "alarm-clock.png"
    ).convert("RGBA")
    data = list(clock_im.getdata())
    new_data = []
    for pixel in data:
        if pixel[3] != 0:
            new_data.append((255, 255, 255, pixel[3]))
        else:
            new_data.append(pixel)  # Keep original
    clock_im.putdata(new_data)
    layer2.paste(clock_im.resize((48, 48)), clock_position)

    font_clock_hour = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Medium.ttf"), 32)
    draw.text(
        (clock_position[0] + 65, clock_position[1] + 5),
        _date(aggregate.closest_webinar_dt, "H:i"),
        font=font_clock_hour,
        fill=(255, 255, 255, 255),
    )

    # User
    user_position = (540, 475)
    user_im = Image.open(ASSETS_DIR / "aggregate_blogpost_banner" / "user.png").convert(
        "RGBA"
    )
    data = list(user_im.getdata())
    new_data = []
    for pixel in data:
        if pixel[3] != 0:
            new_data.append((255, 255, 255, pixel[3]))
        else:
            new_data.append(pixel)  # Keep original
    user_im.putdata(new_data)
    layer2.paste(user_im.resize((48, 48)), user_position)

    font_clock_hour = load_font(str(ASSETS_DIR / "fonts" / "Montserrat-Medium.ttf"), 32)
    draw.text(
        (user_position[0] + 55, user_position[1] + 5),
        aggregate.lecturer.fullname,
        font=font_clock_hour,
        fill=(255, 255, 255, 255),
    )

    # # Clock
    # clock_im = Image.open(
    #     ASSETS_DIR / "aggregate_blogpost_banner" / "alarm-clock.png"
    # ).convert("RGBA")
    # layer2.paste(clock_im, (300, 300))

    # Text

    # DEBUG line
    # draw.line([(75, 120), (75 + 1200, 120)], fill="red", width=5)

    draw = ImageDraw.Draw(layer1)
    font_aggregate_title = load_font(
        str(ASSETS_DIR / "fonts" / "Montserrat-Bold.ttf"), 60
    )
    draw_multiline_text(
        draw,
        font_aggregate_title,
        aggregate.title,
        (75, 120),
        1200,
        fill=(255, 255, 255, 255),
    )

    out = Image.alpha_composite(layer1, layer2)

    # Create byte buffer
    bytes_io = BytesIO()

    # Save PDF bytes to buffer
    out.save(bytes_io, format="PNG", save_all=True)

    # Get and return PDF bytes
    return HttpResponse(bytes_io.getvalue(), content_type="image/png")
