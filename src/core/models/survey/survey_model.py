"""Survey model"""

# flake8: noqa=E501

from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    QuerySet,
    SlugField,
    TextField,
)


class SurveyVoteManager(Manager):
    """SurveyVoteManager"""

    def get_votes_for_answer_and_voter_id(
        self, answer: "SurveyAnswer", voter_id: str
    ) -> QuerySet["SurveyVote"]:
        """get_answers"""
        return self.get_queryset().filter(voter_id=voter_id, answer=answer)


class SurveyVote(Model):
    """SurveyVote"""

    manager = SurveyVoteManager()

    created_at = DateTimeField(auto_now_add=True)

    voter_id = CharField("ID głosującego", max_length=100)

    answer = ForeignKey("SurveyAnswer", on_delete=CASCADE, verbose_name="Odpowiedź")

    class Meta:
        """meta"""

        verbose_name = "Ankieta (głos)"
        verbose_name_plural = "Ankiety (głosy)"

    def __str__(self) -> str:
        return f"{self.voter_id}"


class SurveyAnswerManager(Manager):
    """SurveyAnswerManager"""

    def get_answers_for_survey(self, survey: "Survey") -> QuerySet["SurveyAnswer"]:
        """get_answers"""
        return self.get_queryset().filter(survey=survey)


class SurveyAnswer(Model):
    """SurveyAnswer"""

    manager = SurveyAnswerManager()

    created_at = DateTimeField(auto_now_add=True)

    title = CharField("Tytuł", max_length=250)

    user_created = BooleanField("Dodana przez użytkownika", default=False)

    survey = ForeignKey("Survey", on_delete=CASCADE, verbose_name="Ankieta")

    class Meta:
        """meta"""

        verbose_name = "Ankieta (odpowiedź)"
        verbose_name_plural = "Ankiety (odpowiedzi)"

    def __str__(self) -> str:
        return f"{self.title}"


class SurveyManager(Manager):
    """SurveyManager"""

    ...


class Survey(Model):
    """Survey"""

    manager = SurveyManager()

    created_at = DateTimeField(auto_now_add=True)

    slug = SlugField(
        "Slug ankiety",
        max_length=100,
        blank=False,
        unique=True,
        help_text="Fragment w URL",
    )

    title = CharField("Tytuł", max_length=250)
    description = TextField("Opis", blank=True)

    add_placeholder = CharField(
        "Placeholder add", max_length=128, default="[add_placeholder]"
    )
    search_placeholder = CharField(
        "Placeholder search", max_length=128, default="[search_placeholder]"
    )

    user_creation_enabled = BooleanField(
        "Dodawanie przez użytkownka aktywowane", default=False
    )

    class Meta:
        """meta"""

        verbose_name = "Ankieta"
        verbose_name_plural = "Ankiety"

    def __str__(self) -> str:
        return f"{self.title}"
