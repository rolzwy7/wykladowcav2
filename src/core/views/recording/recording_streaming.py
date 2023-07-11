from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from core.models import WebinarRecordingToken
from core.services import StreamingService


def recording_streaming(request: HttpRequest, uuid: str):
    """Stream recording controller"""

    # Get recording token
    recording_token = get_object_or_404(WebinarRecordingToken, token=uuid)

    # Check if expired, if so then deny access
    # TODO: token expiration

    # Call streaming service
    service = StreamingService(recording_token)
    return service.get_streaming_response(request)
