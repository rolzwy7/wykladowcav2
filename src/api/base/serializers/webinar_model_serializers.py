"""Webinar model serializers"""

from rest_framework import serializers

from core.models import Webinar


class WebinarModelSerializer(serializers.ModelSerializer):
    """Serializer for `Webinar` model"""

    class Meta:
        model = Webinar
        fields = "__all__"
