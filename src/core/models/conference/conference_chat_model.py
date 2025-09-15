"""Conference Chat Model"""

# flake8: noqa=E501

import uuid

from django.db.models import CharField, DateTimeField, Model, UUIDField

from .chat_message_status_enum import MODEL_CHAT_MESSAGE_STATUS, ChatMessageStatusEnum

# Załóżmy, że posiadasz już model Konferencji.
# Jeśli nazywa się inaczej, zmień poniższy import i pole OneToOneField.
# from your_video_conference_app.models import Conference


class ConferenceChat(Model):
    """
    Model reprezentujący pojedynczy chat przypisany do wideokonferencji.
    Używamy OneToOneField, aby zapewnić, że każda konferencja ma dokładnie jeden chat.
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")

    init_status = CharField(
        "Początkowy status wiadomości",
        max_length=32,
        choices=MODEL_CHAT_MESSAGE_STATUS,
        default=ChatMessageStatusEnum.INIT,
    )

    # hide_usernames = BooleanField("Schowaj nazwy użytkowników", default=False)

    class Meta:
        """Meta"""

        verbose_name = "Chat konferencji"
        verbose_name_plural = "Chaty konferencji"

    def __str__(self):
        return f"Chat ID: {self.id}"  # type: ignore
