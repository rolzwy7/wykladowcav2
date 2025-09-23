"""Conference Heartbeat API"""

# flake8: noqa=E501

from django.utils import timezone
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.base.serializers import ConferenceParticipantHeartbeatSerializer
from api.base.throttling import WatchroomHeartbeatAnonRateThrottle
from core.models import ConferenceFreeParticipant


class ConferenceParticipantHeartbeatView(UpdateAPIView):
    """
    Endpoint API do aktualizacji `last_watchroom_heartbeat` dla uczestnika.
    Używa metody PATCH i identyfikuje uczestnika na podstawie `watch_token` z URL.
    """

    queryset = ConferenceFreeParticipant.manager.all()
    serializer_class = ConferenceParticipantHeartbeatSerializer
    throttle_classes = [WatchroomHeartbeatAnonRateThrottle]
    permission_classes = [AllowAny]  # Dostęp publiczny, weryfikacja przez token
    lookup_field = "watch_token"
    lookup_url_kwarg = "watch_token"

    http_method_names = ["patch"]  # Akceptujemy tylko metodę PATCH

    def update(self, request, *args, **kwargs):
        """
        Nadpisuje domyślną metodę update, aby zaktualizować pole
        `last_watchroom_heartbeat` na aktualny czas i zwrócić
        minimalną odpowiedź.
        """
        instance = self.get_object()
        instance.last_watchroom_heartbeat = timezone.now()
        instance.save(update_fields=["last_watchroom_heartbeat"])

        # Zwracamy prostą odpowiedź sukcesu zamiast pełnych danych obiektu
        return Response(
            {"success": True, "status": "heartbeat updated"}, status=status.HTTP_200_OK
        )
