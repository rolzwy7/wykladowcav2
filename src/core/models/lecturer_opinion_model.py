from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    TextField,
)

from .enums import LecturerOpinionRating


class LecturerOpinion(Model):
    """Represents opinion about lecturer"""

    created_at = DateTimeField(auto_now_add=True)

    visible_on_page = BooleanField("Widoczna na stronie", default=False)

    lecturer = ForeignKey(
        "Lecturer", verbose_name="Wykładowca", on_delete=CASCADE
    )

    fullname = CharField("Imię i Nazwisko", max_length=100)

    company_name = CharField("Firma", max_length=200, blank=True)

    job_title = CharField("Stanowisko", max_length=100, blank=True)

    opinion_text = TextField("Treść opinii")

    RATING = [
        (LecturerOpinionRating.START_1, "1 gwiazdka"),
        (LecturerOpinionRating.START_2, "2 gwiazdki"),
        (LecturerOpinionRating.START_3, "3 gwiazdki"),
        (LecturerOpinionRating.START_4, "4 gwiazdki"),
        (LecturerOpinionRating.START_5, "5 gwiazdek"),
    ]

    rating = CharField("Ocena", max_length=16, choices=RATING)

    class Meta:
        verbose_name = "Opinia o wykładowcy"
        verbose_name_plural = "Opinie o wykładowcy"

    def __str__(self) -> str:
        return str(self.fullname)

    @property
    def rating_number(self):
        """Get rating number"""
        return {
            LecturerOpinionRating.START_1: 1,
            LecturerOpinionRating.START_2: 2,
            LecturerOpinionRating.START_3: 3,
            LecturerOpinionRating.START_4: 4,
            LecturerOpinionRating.START_5: 5,
        }[self.rating]
