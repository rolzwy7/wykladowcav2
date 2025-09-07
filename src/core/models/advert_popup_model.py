"""Advert Popup Model"""

# flake8: noqa

# flake8: noqa=E501
# pylint: disable=line-too-long

import uuid

from django.db import models
from django.db.models import (
    CASCADE,
    RESTRICT,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    QuerySet,
    URLField,
    UUIDField,
)
from django.utils import timezone


class AdvertPopupManager(Manager):
    """AdvertPopupManager query Manager"""

    def get_active(self) -> QuerySet["AdvertPopup"]:
        """
        Returns only the popups that are currently active and visible.
        - `is_visible` must be True.
        - `activate_after` must be in the past or null.
        - `disable_after` must be in the future or null.
        """
        now = timezone.now()
        return (
            self.get_queryset()
            .filter(is_visible=True)
            .filter(
                models.Q(activate_after__lte=now)
                | models.Q(activate_after__isnull=True)
            )
            .filter(
                models.Q(disable_after__gte=now) | models.Q(disable_after__isnull=True)
            )
        )


class AdvertPopup(Model):
    """
    Represents a promotional popup that can be displayed on the website.
    Its visibility can be controlled by a date range.
    """

    manager = AdvertPopupManager()

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    is_visible = BooleanField(
        "Widoczny",
        default=True,
        help_text="Zaznacz, aby popup był publicznie widoczny.",
    )

    show_after_seconds = models.PositiveIntegerField(
        "Wyświetl po sekundach",
        default=5,
        help_text="Liczba sekund po załadowaniu strony, po których popup zostanie pokazany. 0 oznacza natychmiast.",
    )

    activate_after = DateTimeField(
        "Aktywuj po dacie",
        null=True,
        blank=True,
        help_text="Popup pojawi się na stronie dopiero po tej dacie. Pozostaw puste, aby aktywować natychmiast.",
    )
    disable_after = DateTimeField(
        "Dezaktywuj po dacie",
        null=True,
        blank=True,
        help_text="Popup zniknie ze strony po tej dacie. Pozostaw puste, aby nigdy nie wygasał.",
    )

    popup_title = CharField(
        "Tytuł popupa",
        max_length=100,
        help_text="Główny tekst, który zobaczy użytkownik (np. 'Nowa promocja!').",
    )
    popup_confirm_btn_text = CharField(
        "Tekst przycisku akcji",
        max_length=50,
        default="Sprawdź",
        help_text="Tekst na przycisku potwierdzającym (np. 'Dowiedz się więcej').",
    )
    popup_cancel_btn_text = CharField(
        "Tekst przycisku anulowania",
        max_length=50,
        default="Zamknij",
        blank=True,
        help_text="Tekst na przycisku zamykającym (np. 'Nie, dziękuję'). Można zostawić puste.",
    )

    image_url = URLField(
        "URL obrazka",
        max_length=512,
        help_text="Link do grafiki wyświetlanej w popupie.",
    )
    target_url = URLField(
        "Docelowy URL",
        max_length=512,
        help_text="Link, na który zostanie przekierowany użytkownik po kliknięciu przycisku akcji.",
    )

    class Meta:
        """Meta"""

        verbose_name = "Advert Popup"
        verbose_name_plural = "Advert Popups"
        ordering = ["-created_at"]

    def __str__(self):
        return self.popup_title


class AdvertPopupClick(Model):
    """Tracks clicks on advertisement popups."""

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = DateTimeField("Data kliknięcia", auto_now_add=True)

    popup = ForeignKey(
        "AdvertPopup",
        on_delete=CASCADE,
        verbose_name="Advert Popup",
    )

    spy_object = ForeignKey(
        "SpyObject",
        on_delete=RESTRICT,
        null=True,
        blank=True,
        verbose_name="Spy Object",
    )

    class Meta:
        """Meta"""

        verbose_name = "Advert Popup Click"
        verbose_name_plural = "Advert Popup Clicks"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Click {self.id}"
