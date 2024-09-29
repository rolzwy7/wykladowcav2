"""survey_api"""

# flake8: noqa=E501

from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.base.serializers import SurveyAnswerSerializer, SurveySerializer
from core.models.survey import Survey, SurveyAnswer, SurveyVote


class SurveyViewSet(ViewSet):
    """SurveyViewSet"""

    queryset = Survey.manager.all()

    def list(self, request):
        """list"""
        serializer = SurveySerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """retrieve"""
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = SurveySerializer(item)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def answers(self, request, pk=None):
        """answers"""
        item = get_object_or_404(self.queryset, pk=pk)
        answers = SurveyAnswer.manager.get_answers_for_survey(item)
        serializer = SurveyAnswerSerializer(answers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def vote(self, request, pk=None):
        """answers"""
        # Get survey
        item = get_object_or_404(self.queryset, pk=pk)

        # Prepare variables
        answer_id: int = request.data["answer_id"]
        voter_id: str = request.data["voter_id"]

        # Get answer
        answers = SurveyAnswer.manager.get_answers_for_survey(item).filter(id=answer_id)
        answer = answers.first()
        if not answer:
            return Response({"ok": False})

        # Vote
        qs = SurveyVote.manager.get_votes_for_answer_and_voter_id(answer, voter_id)
        vote = qs.first()
        if vote:
            vote.delete()
            return Response({"action": "deleted"})
        else:
            SurveyVote(voter_id=voter_id, answer=answer).save()
            return Response({"action": "added"})

    @action(url_path="vote-custom", detail=True, methods=["post"])
    def vote_custom(self, request, pk=None):
        """answers"""
        return Response({"ok": True})
