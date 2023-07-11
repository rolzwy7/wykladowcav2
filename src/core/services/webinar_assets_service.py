from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from core.models import Webinar, WebinarAsset

MEDIA_ROOT = settings.MEDIA_ROOT


class WebinarAssetsService:
    def __init__(self, webinar: Webinar) -> None:
        self.webinar = webinar

    def save_asset(self, file: UploadedFile):
        """Save uploaded asset in database"""
        asset = WebinarAsset(
            webinar=self.webinar,
            filename=file.name,
            filesize=str(file.size),
            content_type=file.content_type,
            file=file,
        )
        asset.save()
