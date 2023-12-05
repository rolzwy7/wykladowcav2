"""
Pillow utils functions for text placement
"""

from PIL import Image, ImageDraw, ImageFont


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    template_layer: Image.Image,
    font: ImageFont.FreeTypeFont,
    text: str,
    /,
    *,
    x: int = 0,  # pylint: disable=invalid-name
    y: int = 0,  # pylint: disable=invalid-name
    fill: tuple[int, int, int, int] = (0, 0, 0, 255),
):
    """Place text in relation to image center

    Args:
        draw (ImageDraw.ImageDraw): draw object
        template_layer (Image.Image): template layer
        font (ImageFont.FreeTypeFont): font object
        text (str): text to be placed
        x (int): offset for X axis
        y (int): offset for Y axis
        fill (tuple): RGBA color fill
    """
    ts_w, ts_h = draw.textsize(text, font=font)  # type: ignore

    draw.text(
        (
            x + ((template_layer.width - ts_w) / 2),
            y + ((template_layer.height - ts_h) / 2),
        ),
        text,
        fill=fill,
        font=font,
    )


def draw_multiline_centered_text(
    draw: ImageDraw.ImageDraw,
    template_layer: Image.Image,
    font: ImageFont.FreeTypeFont,
    text: str,
    /,
    *,
    x: int = 0,  # pylint: disable=invalid-name
    x_delta: int = 0,
    y: int = 0,  # pylint: disable=invalid-name
    y_delta: int = 50,
    fill: tuple[int, int, int, int] = (0, 0, 0, 255),
    max_width_px: int = 1000,
):
    """Place multiline text in relation to center

    Args:

        draw (ImageDraw.ImageDraw): draw object
        template_layer (Image.Image): template layer
        font (ImageFont.FreeTypeFont): font object
        text (str): text to be placed
        x (int): offset for X axis
        x_delta (int): offset delta for X axis for each next line
        y (int): offset for Y axis
        y_delta (int): offset delta for Y axis for each next line
        fill (tuple): RGBA color fill
        max_width_px (int): max width allowed for each line in pixels
    """

    stop_flag = "@@STOP"
    words = text.split(" ")  # split into words
    words.append(stop_flag)  # add stop flag at the end
    words = list(reversed(words))  # reverse list for pop() method
    line_seq = []
    y_offset = 0  # Y offset for each line
    x_offset = 0  # X offset for each line

    while words:
        word = words.pop()  # get next word

        if word == stop_flag:
            # Draw last line and return
            line_str = " ".join(line_seq)
            draw_centered_text(
                draw,
                template_layer,
                font,
                line_str,
                x=x + x_offset,
                y=y + y_offset,
                fill=fill,
            )
            return
        else:
            line_seq.append(word)

        line_str = " ".join(line_seq)
        ts_w, _ = draw.textsize(line_str, font=font)  # type: ignore

        if ts_w > max_width_px:
            # Calculate max line ratio for this line candidate
            max_line_ratio = ts_w / max_width_px

            # If line ratio is greater then set maximum allowed
            # then pop last word and save it for next
            if max_line_ratio >= 1.2:
                corrected_word = line_seq.pop()
                line_str = " ".join(line_seq)  # update line str
                # update text width
                ts_w, _ = draw.textsize(line_str, font=font)  # type: ignore
            else:
                corrected_word = None

            draw_centered_text(
                draw,
                template_layer,
                font,
                line_str,
                x=x + x_offset,
                y=y + y_offset,
                fill=fill,
            )
            line_seq = []  # reset line sequence
            if corrected_word:
                line_seq.append(corrected_word)
            y_offset += y_delta  # update Y offset
            x_offset += x_delta  # update X offset


def draw_multiline_text(
    draw: ImageDraw.ImageDraw,
    font: ImageFont.FreeTypeFont,
    text: str,
    position: tuple[int, int],
    max_width_px: int,
    /,
    *,
    fill: tuple[int, int, int, int] = (0, 0, 0, 255),
):
    """Draw multi line text starting from given (X,Y) coordinates"""
    words = text.split()
    lines = []
    current_line = words[0]
    x, y = position  # pylint: disable=invalid-name

    for word in words[1:]:
        test_line = current_line + " " + word
        width = draw.textlength(test_line, font=font)

        if width <= max_width_px:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        # Move down for the next line
        y += font.size  # pylint: disable=invalid-name
