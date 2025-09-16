"""
Widoki API (endpoints) dla czatu konferencji.
"""

# flake8: noqa=E501
# pylint: disable=missing-function-docstring

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.base.serializers import (
    ChatMessageStatusUpdateSerializer,
    ConferenceChatMessageCreateSerializer,
    ConferenceChatMessageSerializer,
    ModeratorChatMessageSerializer,
)
from api.base.throttling import ChatMessageAnonRateThrottle
from core.models import ConferenceChat, ConferenceChatMessage, ConferenceFreeParticipant
from core.models.conference.chat_message_status_enum import ChatMessageStatusEnum


class ChatMessageListView(APIView):
    """
    Widok API do pobierania listy wiadomości dla danego czatu.
    Wyświetla tylko wiadomości, które zostały zaakceptowane.
    """

    permission_classes = [AllowAny]

    def get(self, request, chat_id, format=None):
        """
        Zwraca listę zaakceptowanych wiadomości dla czatu o podanym ID.
        """
        # Upewniamy się, że czat istnieje
        chat = get_object_or_404(ConferenceChat, id=chat_id)

        # Pobieramy tylko wiadomości z statusem 'ACCEPTED'
        messages = ConferenceChatMessage.objects.filter(
            chat=chat, status=ChatMessageStatusEnum.ACCEPTED
        ).order_by("created_at")

        serializer = ConferenceChatMessageSerializer(messages, many=True)
        return Response(serializer.data)


class ChatMessageCreateView(APIView):
    """
    Widok API do tworzenia nowej wiadomości na czacie.
    Wymaga tokenu uczestnika (`watch_token`) do identyfikacji autora.
    """

    permission_classes = [AllowAny]
    throttle_classes = [ChatMessageAnonRateThrottle]

    def post(self, request, chat_id, format=None):
        """
        Tworzy nową wiadomość na czacie.
        """
        chat = get_object_or_404(ConferenceChat, id=chat_id)
        serializer = ConferenceChatMessageCreateSerializer(data=request.data)

        # Token identyfikujący użytkownika, przesyłany w nagłówku
        watch_token = request.headers.get("X-Watch-Token")
        if not watch_token:
            return Response(
                {"error": "Brak tokenu identyfikacyjnego (X-Watch-Token)."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            participant = ConferenceFreeParticipant.manager.get(watch_token=watch_token)
        except ConferenceFreeParticipant.DoesNotExist:
            return Response(
                {"error": "Nie znaleziono uczestnika dla podanego tokenu."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if serializer.is_valid():
            # Tworzymy i zapisujemy wiadomość, przekazując dodatkowe pola do metody save()
            message_instance = serializer.save(
                chat=chat,
                chat_user=participant,
                status=chat.init_status,  # Ustawiamy status początkowy z konfiguracji czatu
            )

            # Zwracamy dane nowo utworzonej wiadomości
            response_serializer = ConferenceChatMessageSerializer(message_instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModerationMessageListView(APIView):
    """
    Zwraca listę wiadomości oczekujących na ręczną moderację
    dla danego czatu. Wymaga uprawnień administratora.
    """

    permission_classes = [IsAdminUser]

    def get(self, request, chat_id, format=None):
        chat = get_object_or_404(ConferenceChat, id=chat_id)
        messages = ConferenceChatMessage.objects.filter(
            chat=chat, status=ChatMessageStatusEnum.MANUAL_ADMIN
        ).order_by("created_at")

        serializer = ModeratorChatMessageSerializer(messages, many=True)
        return Response(serializer.data)


class ModerationMessageUpdateView(APIView):
    """
    Aktualizuje status pojedynczej wiadomości (akceptuje lub odrzuca).
    Wymaga uprawnień administratora.
    """

    permission_classes = [IsAdminUser]

    def patch(self, request, message_id, format=None):
        message = get_object_or_404(ConferenceChatMessage, id=message_id)
        serializer = ChatMessageStatusUpdateSerializer(
            instance=message, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
