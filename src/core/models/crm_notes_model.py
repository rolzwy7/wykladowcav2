"""crm_notes_model"""

# flake8: noqa=E501

from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    Manager,
    Model,
    Q,
    QuerySet,
    TextField,
)
from django.utils.timezone import now


class CrmNoteManager(Manager):
    """CrmNoteManager"""

    def get_notes(self) -> QuerySet["CrmNote"]:
        """Get visible categories"""
        return self.get_queryset().filter(
            Q(hide=False)
            & (Q(show_after=None) | Q(show_after__lt=now()))
            & (Q(hide_after=None) | Q(hide_after__gt=now()))
        )


class CrmNote(Model):
    """Metadat for Webinar model"""

    manager = CrmNoteManager()

    created_at = DateTimeField(auto_now_add=True)

    hide = BooleanField(default=False)
    show_after = DateTimeField(blank=True, null=True)
    hide_after = DateTimeField(blank=True, null=True)
    deadline = DateTimeField(blank=True, null=True)

    note_title = TextField("Tytuł (HTML)")
    note_content_html = TextField("Treść (HTML)", blank=True)

    COLORS = [
        ("primary", "primary"),
        ("secondary", "secondary"),
        ("success", "success"),
        ("danger", "danger"),
        ("warning", "warning"),
        ("info", "info"),
    ]
    color = CharField("Kolor", max_length=32, default="primary", choices=COLORS)

    @property
    def deadline_progress_base_days(self):
        """deadline_progress_base_days"""
        if self.deadline:
            return max((self.deadline - self.created_at).days, 0)
        return None

    @property
    def deadline_progress_remaining_days(self):
        """deadline_progress_remaining_days"""

        if self.deadline:
            delta = self.deadline - now()
            return max(delta.days, 0)  # Ensure non-negative days

        return None

    @property
    def deadline_progress_percent(self):
        """deadline_progress_percent"""
        if self.deadline_progress_remaining_days and self.deadline_progress_base_days:
            prct = (
                self.deadline_progress_remaining_days / self.deadline_progress_base_days
            )
            return int(round(prct * 100, 2))
        else:
            return None

    @property
    def deadline_progress_color(self):
        """deadline_progress_color"""
        if self.deadline_progress_percent:
            if self.deadline_progress_percent > 70:
                return "success"
            elif self.deadline_progress_percent > 50:
                return "warning"
            else:
                return "danger"
        return None
