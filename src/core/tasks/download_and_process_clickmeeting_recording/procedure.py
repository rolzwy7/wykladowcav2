import logging
from pathlib import Path

import requests
from django.conf import settings
from requests.exceptions import HTTPError

from core.libs.clickmeeting import list_clickmeeting_room_recordings
from core.models import Webinar, WebinarMetadata, WebinarRecording
from core.models.enums import WebinarRecordingStatus

logger = logging.getLogger(
    "core.tasks.download_and_process_clickmeeting_recording"
)


def download_recording(
    recording_id: str, recording_url: str, recording_file_size: str
):
    """Download recording to media directory"""
    chunk_size = 1024 * 200
    base_dir = Path(settings.MEDIA_ROOT, "recordings")
    base_dir.mkdir(exist_ok=True)
    filepath = base_dir / f"{recording_id}.mp4"
    filesize = int(recording_file_size)
    downloaded = 0
    with requests.get(recording_url, stream=True, timeout=10) as response:
        response.raise_for_status()
        with filepath.open("wb") as dst:
            for chunk in response.iter_content(chunk_size=chunk_size):
                downloaded += len(chunk)
                logger.info(
                    "download_recording progress %s/%s (%s)",
                    downloaded,
                    filesize,
                    f"{downloaded/filesize:.2%}",
                )
                dst.write(chunk)


def download_and_process_clickmeeting_recording(webinar_id: int) -> str:
    """Downloads and processes Clickmeeting recording"""

    # Get webinar by id
    webinar = Webinar.manager.get(id=webinar_id)

    # Get webinar metadata by webinar
    webinar_metadata = WebinarMetadata.objects.get(webinar=webinar)

    # Get clickmeeting room id from metadata
    clickmeeting_id = webinar_metadata.clickmeeting_id

    # Room id might not be set in metadata (inpropable but not impossible)
    if not clickmeeting_id:
        return "No `clickmeeting_id` in metadata"

    recordings = list_clickmeeting_room_recordings(int(clickmeeting_id))

    # There are no recordings for given webinar
    if len(recordings) == 0:
        return "No recordings"

    # Iterate over Clickmeeting recordings
    for recording in recordings:
        # Check if recording exists
        recording_exists = WebinarRecording.manager.filter(
            recording_id=recording.id
        ).exists()

        # Get or create recording
        if recording_exists:
            db_recording = WebinarRecording.manager.get(
                recording_id=str(recording.id)
            )
            # Update recording download url
            db_recording.recording_url = recording.recording_url
            db_recording.save()
        else:
            db_recording = WebinarRecording(
                webinar=webinar,
                recording_id=str(recording.id),
                recording_url=recording.recording_url,
                recording_duration_seconds=recording.recording_duration,
                recorder_started=recording.recorder_started,
                recording_file_size=recording.recording_file_size,
                recording_name=recording.recording_name,
            )
            db_recording.save()

        # Skip if recording already downloaded
        if db_recording.status == WebinarRecordingStatus.DOWNLOADED:
            continue

        # Download recording
        try:
            download_recording(
                db_recording.recording_id,
                db_recording.recording_url,
                db_recording.recording_file_size,
            )
        except HTTPError:
            db_recording.status = WebinarRecordingStatus.FAILED
            db_recording.save()
        else:
            db_recording.status = WebinarRecordingStatus.DOWNLOADED
            db_recording.save()

    return "Finished"
