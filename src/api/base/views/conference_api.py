"""Conference API"""

# flake8: noqa=E501

from django.conf import settings
from django.urls import reverse
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

    if edition.start_redirecting_participants and edition.stream_url_page:
        watch_url = f"{settings.BASE_URL}" + reverse(
            "core:conference_waiting_room_page",
            kwargs={"watch_token": participant.watch_token},
        )
    else:
        watch_url = ""

    # If `watch_url` is empty there will be no redirect to watch room
    return Response({"watch_url": watch_url})
