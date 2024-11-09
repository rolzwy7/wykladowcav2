"""Surveey serializers"""

# flake8: noqa=E501

from django.conf import settings
from django.db.models import Q
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.models.survey import Survey, SurveyAnswer, SurveyVote


class SurveySerializer(ModelSerializer):
    """SurveySerializer"""

    class Meta:
        """meta"""

        model = Survey
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "user_creation_enabled",
            "add_placeholder",
            "search_placeholder",
        ]


class SurveyAnswerSerializer(ModelSerializer):
    """SurveyAnswerSerializer"""

    vote_percent = SerializerMethodField()
    init_checked = SerializerMethodField()
    image = SerializerMethodField()

    user_creation_enabled = SerializerMethodField()
    avatar_placeholders_enabled = SerializerMethodField()
    ask_about_opinion_enabled = SerializerMethodField()

    class Meta:
        """Meta"""

        model = SurveyAnswer
        fields = [
            "id",
            "title",
            "user_created",
            "vote_percent",
            "init_checked",
            "image",
            "user_creation_enabled",
            "avatar_placeholders_enabled",
            "ask_about_opinion_enabled",
        ]

    def __init__(self, *args, **kwargs):
        # Accept a custom parameter 'user_id' and make it available in the instance
        self.voter_id = kwargs.pop("voter_id", None)
        super(SurveyAnswerSerializer, self).__init__(*args, **kwargs)

    def get_init_checked(self, answer: SurveyAnswer):
        """Check if answer is already checked for this voter id"""
        return SurveyVote.manager.filter(
            Q(voter_id=self.voter_id) & Q(answer=answer)
        ).exists()

    def get_vote_percent(self, answer: SurveyAnswer):
        """Get percentage of all votes that this answer got"""
        all_votes_count = SurveyVote.manager.filter(
            answer__survey=answer.survey
        ).count()
        this_answer_count = SurveyVote.manager.filter(answer=answer).count()

        if all_votes_count == 0:
            return 0

        return int(100 * (this_answer_count / all_votes_count))

    def get_image(self, answer: SurveyAnswer):
        """Check image"""

        if answer.lecturer:
            return f"{settings.BASE_URL}{settings.MEDIA_URL}uploads/lecturers/{answer.lecturer.slug}_160x160.webp"
        else:
            if answer.survey.avatar_placeholders_enabled:
                return f"{settings.BASE_URL}/static/media/images/avatar_160x160.jpg"

        return "no_image"

    def get_user_creation_enabled(self, answer: SurveyAnswer):
        """user_creation_enabled"""
        return answer.survey.user_creation_enabled

    def get_avatar_placeholders_enabled(self, answer: SurveyAnswer):
        """avatar_placeholders_enabled"""
        return answer.survey.avatar_placeholders_enabled

    def get_ask_about_opinion_enabled(self, answer: SurveyAnswer):
        """ask_about_opinion_enabled"""
        return answer.survey.ask_about_opinion_enabled
