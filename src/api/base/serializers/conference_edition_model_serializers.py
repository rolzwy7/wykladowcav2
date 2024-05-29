"""Webinar model serializers"""

from rest_framework import serializers

from core.models import ConferenceEdition


class ConferenceEditionSerializer(serializers.ModelSerializer):
    """Serializer for `ConferenceEdition` model"""

    class Meta:
        model = ConferenceEdition
        fields = "__all__"
