"""
Pillow utils for font loading
"""

from pathlib import Path

from django.conf import settings
from PIL import ImageFont

BASE_DIR = settings.BASE_DIR
ASSETS_DIR: Path = BASE_DIR.parent / "core" / "assets"


def load_font(font_name: str, font_size: int):
    """Load font from assets directory"""
    font_path = ASSETS_DIR / "fonts" / font_name
    return ImageFont.truetype(str(font_path), font_size)
