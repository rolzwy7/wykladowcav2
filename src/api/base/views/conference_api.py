"""Conference API"""

# flake8: noqa=E501

from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from core.models import ConferenceFreeParticipant


@api_view(["GET"])
@renderer_classes([JSONRenderer])
def conference_watch_url(request, uuid: str):
    """Return conference URL using participant UUID"""

    participant = ConferenceFreeParticipant.manager.filter(watch_token=uuid).first()

    if not participant:
        return Response(
            {"error": "Invalid watch token"}, status=status.HTTP_400_BAD_REQUEST
        )

    edition = participant.edition

    if not edition:
        return Response(
            {"error": "Edition not linked"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response({"watch_url": edition.stream_url_page})
