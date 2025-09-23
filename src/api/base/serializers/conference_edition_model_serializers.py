"""Webinar model serializers"""

# flake8: noqa=E501

from rest_framework import serializers

from core.models import ConferenceEdition, ConferenceFreeParticipant


class ConferenceEditionSerializer(serializers.ModelSerializer):
    """Serializer for `ConferenceEdition` model"""

    class Meta:
        model = ConferenceEdition
        fields = "__all__"


class ConferenceParticipantHeartbeatSerializer(serializers.ModelSerializer):
    """
    Serializer do aktualizacji heartbeat uczestnika.
    Jest to pusty serializer, ponieważ nie przyjmujemy żadnych danych w ciele żądania.
    Logika aktualizacji czasu znajduje się w widoku.
    """

    class Meta:
        model = ConferenceFreeParticipant
        fields = []  # Nie oczekujemy żadnych pól w ciele żądania PATCH
