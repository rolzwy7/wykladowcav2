"""
Model that represents opinion about given lecturer
"""

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
    TextField,
)

from .enums import LecturerOpinionRating
from .lecturer_model import Lecturer


class LecturerOpinionManager(Manager):
    """Lecturer opinion query Manager"""

    def get_all_visible_opinions(self) -> QuerySet["LecturerOpinion"]:
        """Get all opinions that are visible on website"""
        return self.get_queryset().filter(visible_on_page=True)

    def get_visible_opinions_for_lecturer(
        self, lecturer: Lecturer
    ) -> QuerySet["LecturerOpinion"]:
        """Get opinions for lecturer that are marked as visible on page"""
        return self.get_all_visible_opinions().filter(lecturer=lecturer)


class LecturerOpinion(Model):
    """Represents opinion about lecturer"""

    manager = LecturerOpinionManager()

    created_at = DateTimeField(auto_now_add=True)

    visible_on_page = BooleanField("Widoczna na stronie (Zatwierdzona)", default=False)

    added_on_website = BooleanField("Dodana przez stronę", default=False)

    lecturer = ForeignKey("Lecturer", verbose_name="Wykładowca", on_delete=CASCADE)

    fullname = CharField("Imię i Nazwisko", max_length=100)

    company_name = CharField("Firma", max_length=200, blank=True)

    job_title = CharField("Stanowisko", max_length=100, blank=True)

    opinion_text = TextField("Treść opinii")

    RATING = [
        (LecturerOpinionRating.STARS_1, "1 gwiazdka"),
        (LecturerOpinionRating.STARS_2, "2 gwiazdki"),
        (LecturerOpinionRating.STARS_3, "3 gwiazdki"),
        (LecturerOpinionRating.STARS_4, "4 gwiazdki"),
        (LecturerOpinionRating.STARS_5, "5 gwiazdek"),
    ]

    rating = CharField("Ocena", max_length=16, choices=RATING)

    opinion_hash = CharField("HASH", max_length=100, blank=True)

    class Meta:
        verbose_name = "Opinia o wykładowcy"
        verbose_name_plural = "Opinie o wykładowcy"

        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.fullname)

    @property
    def rating_number(self):
        """Get rating number"""
        return {
            LecturerOpinionRating.STARS_1: 1,
            LecturerOpinionRating.STARS_2: 2,
            LecturerOpinionRating.STARS_3: 3,
            LecturerOpinionRating.STARS_4: 4,
            LecturerOpinionRating.STARS_5: 5,
        }[self.rating]

    @property
    def rating_sequence(self):
        """Get rating sequence for opinions"""
        return [1, 2, 3, 4, 5]
