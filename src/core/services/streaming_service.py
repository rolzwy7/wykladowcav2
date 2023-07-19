import os
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from core.models import WebinarRecording, WebinarRecordingToken


class ChunkConfig(BaseModel):
    """Streaming chunk representation"""

    chunk_start: int
    chunk_end: int
    chunk_size: int
    filesize_bytes: int


class StreamingService:
    """Streaming service"""

    def __init__(self, recording_token: WebinarRecordingToken) -> None:
        self.recording_token = recording_token
        self.recording: WebinarRecording = recording_token.recording

    def get_recording_filepath(self) -> Path:
        """Get recording `Path` object"""
        return Path(
            settings.MEDIA_ROOT,
            "recordings",
            f"{self.recording.recording_id}.mp4",
        )

    def is_token_valid(self) -> bool:
        """Check if streaming token is valid

        Returns:
            bool: True if is valid, False otherwise
        """

        # Deny access if denied manually by checkbox
        deny_access = self.recording_token.deny_access
        if deny_access:
            return False

        # Check if token expires
        # If expired then deny access
        expires_at = self.recording_token.expires_at
        if expires_at and now() > expires_at:
            return False

        return True

    def get_streaming_response(self, request: HttpRequest):
        """Get HTTP response to answer video player video request"""

        # Get chunk config
        chunk_config = self.get_chunk_config(request)

        # Open recording file
        recording_filepath = self.get_recording_filepath()
        src = recording_filepath.open("rb")

        # Seek `chunk_start` byte
        src.seek(chunk_config.chunk_start)

        # Read
        buffer = BytesIO(src.read(chunk_config.chunk_size))

        # Close recording file
        src.close()

        # Create streaming response - HTTP 206 Partial Content
        response = HttpResponse(buffer.read(), status=206)

        # Set reponse headers
        response["Content-Length"] = chunk_config.chunk_size
        response["Content-Type"] = "video/mp4"
        response["Accept-Ranges"] = "bytes"
        chunk_start = chunk_config.chunk_start
        chunk_end = chunk_config.chunk_end
        file_size = chunk_config.filesize_bytes
        content_range = f"bytes {chunk_start}-{chunk_end}/{file_size}"
        response["Content-Range"] = content_range

        return response

    def get_chunk_config(self, request: HttpRequest) -> ChunkConfig:
        """Get video streaming chunk config

        Get chunk config used in recording video streaming

        Args:
            request (HttpRequest): http request
            recording_filepath (Path): filepath to recording

        Returns:
            ChunkConfig: chunk config object
        """

        # Get recording size in bytes
        recording_filepath = self.get_recording_filepath()
        filesize_bytes = os.stat(recording_filepath).st_size

        # Save global chunk size setting to local variable
        max_chunk_bytes = settings.STREAMING_CHUNK_SIZE_KB * 1024  # MB

        # Get `Range` header. It is a value that video player is asking for.
        # URL: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range
        # For example: "bytes=0-" is send at the beginning video start
        http_range = request.META["HTTP_RANGE"]  # "bytes=X-Y"

        # Split by equal sign. We don't care about unit type
        _, bytes_range = http_range.split("=")

        # Get bytes range start and end
        range_start, range_end = bytes_range.split("-")

        # Must be convertable to integer
        range_start = int(range_start)
        # range_end = int(range_end)

        # Define chunk start
        chunk_start = range_start

        # Define chunk end
        is_within_range = chunk_start + max_chunk_bytes < filesize_bytes - 1
        if is_within_range:
            chunk_end = chunk_start + max_chunk_bytes
        else:
            chunk_end = filesize_bytes - 1

        # Define chunk size
        chunk_size = (chunk_end - chunk_start) + 1

        return ChunkConfig(
            chunk_start=chunk_start,
            chunk_end=chunk_end,
            chunk_size=chunk_size,
            filesize_bytes=filesize_bytes,
        )
