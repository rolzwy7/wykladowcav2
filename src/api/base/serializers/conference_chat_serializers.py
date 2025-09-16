"""
Serializery dla modeli związanych z czatem konferencji.
"""

# flake8: noqa=E501
# pylint: disable=missing-class-docstring

from rest_framework import serializers

from core.models import ConferenceChatMessage, ConferenceFreeParticipant
from core.models.conference.chat_message_status_enum import ChatMessageStatusEnum


class ConferenceFreeParticipantSerializer(serializers.ModelSerializer):
    """
    Podstawowy serializer dla uczestnika konferencji,
    używany do wyświetlania jego nazwy.
    """

    class Meta:
        model = ConferenceFreeParticipant
        fields = ["first_name"]


class ConferenceChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer do wyświetlania wiadomości na czacie.
    Zawiera zagnieżdżone informacje o autorze wiadomości.
    """

    chat_user = ConferenceFreeParticipantSerializer(read_only=True)
    # Formatowanie daty, aby była bardziej czytelna na froncie
    created_at = serializers.DateTimeField(format="%H:%M:%S")  # type: ignore

    class Meta:
        model = ConferenceChatMessage
        fields = ["id", "chat_user", "message", "created_at"]


class ConferenceChatMessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer używany wyłącznie do tworzenia nowej wiadomości.
    Wymaga tylko treści wiadomości.
    """

    class Meta:
        model = ConferenceChatMessage
        fields = ["message"]


class ModeratorChatMessageSerializer(serializers.ModelSerializer):
    """
    Rozszerzony serializer wiadomości na potrzeby panelu moderacji.
    Wyświetla dodatkowe informacje, takie jak wynik analizy Perspective API.
    """

    chat_user = ConferenceFreeParticipantSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")  # type: ignore

    class Meta:
        model = ConferenceChatMessage
        fields = [
            "id",
            "chat_user",
            "message",
            "created_at",
            "status",
            "perspective_score",
        ]


class ChatMessageStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer do aktualizacji statusu wiadomości przez moderatora.
    """

    class Meta:
        model = ConferenceChatMessage
        fields = ["status"]

    def validate_status(self, value):
        """
        Sprawdza, czy nowy status jest jednym z dozwolonych
        przez moderatora (ACCEPTED lub REJECTED).
        """
        if value not in [
            ChatMessageStatusEnum.ACCEPTED,
            ChatMessageStatusEnum.REJECTED,
        ]:
            raise serializers.ValidationError(
                "Niedozwolona zmiana statusu. Dozwolone: ACCEPTED, REJECTED."
            )
        return value
