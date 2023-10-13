from pathlib import Path

from django.conf import settings
from PIL import Image

from core.models import Lecturer

MEDIA_ROOT = settings.MEDIA_ROOT


def create_thumbnails_for_lecturer(image_path: str, lecturer: Lecturer):
    """Create thumbnails for lecturer"""
    media_root = MEDIA_ROOT
    filepath = Path(media_root, image_path)
    dirpath = filepath.parent

    for width, height in settings.THUMBNAIL_SIZES:
        destination_path = Path(
            dirpath, f"{lecturer.slug}_{width}x{height}.webp"
        )
        with Image.open(str(filepath)) as image:
            image.thumbnail((width, height))
            image.save(destination_path, quality=100)
