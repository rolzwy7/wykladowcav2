from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from core.models import WebinarRecordingToken
from core.services import StreamingService


def recording_streaming(request: HttpRequest, uuid: str):
    """Stream recording controller"""

    # Get recording token
    recording_token = get_object_or_404(WebinarRecordingToken, token=uuid)
    streaming_service = StreamingService(recording_token)

    if not streaming_service.is_token_valid():
        raise PermissionDenied()

    # Call streaming service
    return streaming_service.get_streaming_response(request)
