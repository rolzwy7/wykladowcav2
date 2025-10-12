"""API urls"""

# flake8: noqa=E501

from django.urls import include, path

from api.base.routers import router
from api.base.views import (
    ChatMessageCreateView,
    ChatMessageListView,
    ConferenceParticipantHeartbeatView,
    ModerationMessageListView,
    ModerationMessageUpdateView,
    conference_watch_url,
    create_aggregate_pod_zamkniete,
    fakturownia_sale_recording_webhook,
    health_check,
    regon_autocomplete,
    sale_recording_check_payment_url,
)

app_name = "api"  # pylint: disable=invalid-name

urlpatterns = [
    path("regon-autocomplete/", regon_autocomplete, name="regon-autocomplete"),
    path("health-check/", health_check, name="health-check"),
    path(
        "fakturownia-sale-recording-webhook/",
        fakturownia_sale_recording_webhook,
        name="fakturownia_sale_recording_webhook",
    ),
    path(
        "sale_recording_check_payment_url/<uuid:uuid>/",
        sale_recording_check_payment_url,
        name="sale_recording_check_payment_url",
    ),
    path(
        "conference-watch-url/<uuid:uuid>/",
        conference_watch_url,
        name="conference-watch-url",
    ),
    # Endpoint do pobierania wiadomości
    # np. /api/chat/a1b2c3d4-e5f6-7890-1234-567890abcdef/messages/
    path(
        "chat/<uuid:chat_id>/messages/",
        ChatMessageListView.as_view(),
        name="chat-message-list",
    ),
    # Endpoint do tworzenia wiadomości
    # np. /api/chat/a1b2c3d4-e5f6-7890-1234-567890abcdef/messages/create/
    path(
        "chat/<uuid:chat_id>/messages/create/",
        ChatMessageCreateView.as_view(),
        name="chat-message-create",
    ),
    # Endpoint do pobierania listy wiadomości do moderacji
    # np. /api/moderation/chat/a1b2c3d4-e5f6-7890-1234-567890abcdef/messages/
    path(
        "moderation/chat/<uuid:chat_id>/messages/",
        ModerationMessageListView.as_view(),
        name="moderation-message-list",
    ),
    # Endpoint do aktualizacji statusu wiadomości (akceptacja/odrzucenie)
    # np. /api/moderation/message/a1b2c3d4-e5f6-7890-1234-567890abcdef/update/
    path(
        "moderation/message/<uuid:message_id>/update/",
        ModerationMessageUpdateView.as_view(),
        name="moderation-message-update",
    ),
    path(
        "participant/heartbeat/<uuid:watch_token>/",
        ConferenceParticipantHeartbeatView.as_view(),
        name="participant-heartbeat",
    ),
    path(
        "agregat-pod-zamkniete/",
        create_aggregate_pod_zamkniete,
        name="create_aggregate_pod_zamkniete",
    ),
    path("", include(router.urls)),
]
