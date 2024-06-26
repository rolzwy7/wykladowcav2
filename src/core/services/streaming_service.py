# flake8: noqa:E501
# pylint: disable=line-too-long

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
        self.is_contributor = False

    def get_recording_filepath(self) -> Path:
        """Get recording `Path` object"""
        return Path(
            settings.MEDIA_ROOT,
            "recordings",
            f"{self.recording.recording_id}.mp4",
        )

    def set_is_contributor(self, flag: bool):
        """Set service for contributor"""
        self.is_contributor = flag

    def is_token_valid(self) -> bool:
        """Check if streaming token is valid

        Returns:
            bool: True if is valid, False otherwise
        """

        #  Always valid for contributor
        if self.is_contributor:
            return True

        # Deny access if denied manually by checkbox
        if self.is_access_denied():
            return False

        # Check if token expires
        # If expired then deny access
        if self.is_token_expired():
            return False

        return True

    def is_token_expired(self) -> bool:
        """Check if token expired

        Returns:
            bool: True if is expired, False otherwise
        """
        expires_at = self.recording_token.expires_at

        #  Never expired for contributor
        if self.is_contributor:
            return False

        if expires_at and now() > expires_at:
            return True

        return False

    def is_access_denied(self) -> bool:
        """Check if access is denied for this token

        Returns:
            bool: True if is denied, False otherwise
        """

        #  Never denied for contributor
        if self.is_contributor:
            return False

        return self.recording_token.deny_access

    def is_free_access(self) -> bool:
        """Check if recording is in free access

        Returns:
            bool: True if is in free access, False otherwise
        """
        return self.recording_token.free_access

    def is_password_access(self) -> bool:
        """Check if recording is protected by password

        Returns:
            bool: True if is protected by password, False otherwise
        """
        return self.recording_token.password != ""

    def is_password_correct(self, user_password: str) -> bool:
        """Check if user provided passwords is correct

        Returns:
            bool: True if is correct, False otherwise
        """
        return self.recording_token.password == user_password

    def is_participant_access(self) -> bool:
        """Check if recording is protected by participant login

        Returns:
            bool: True if is protected by participant login, False otherwise
        """
        return self.recording_token.participant is not None

    def is_participant_email_correct(self, email: str) -> bool:
        """Check if recording given email is the same as participant email

        Returns:
            bool: True if it is, False otherwise
        """

        # Always correct for participant
        if self.is_contributor:
            return True

        participant_email: str = self.recording_token.participant.email  # type: ignore
        return participant_email == email

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
