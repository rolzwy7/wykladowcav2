from rest_framework.serializers import ModelSerializer

from core.models.survey import Survey, SurveyAnswer


class SurveySerializer(ModelSerializer):
    class Meta:
        model = Survey
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "user_creation_enabled",
        ]


class SurveyAnswerSerializer(ModelSerializer):
    class Meta:
        model = SurveyAnswer
        fields = [
            "id",
            "title",
            "user_created",
        ]
