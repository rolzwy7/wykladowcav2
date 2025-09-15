"""Conference chat message"""

# flake8: noqa=E501

import uuid

from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    PositiveSmallIntegerField,
    TextField,
    UUIDField,
)

from .chat_message_status_enum import MODEL_CHAT_MESSAGE_STATUS


class ConferenceChatMessage(Model):
    """
    Model reprezentujący pojedynczą wiadomość na chacie konferencji.
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = DateTimeField(auto_now_add=True, verbose_name="Data wysłania")

    chat = ForeignKey(
        "ConferenceChat",
        on_delete=CASCADE,
        related_name="chat",
        verbose_name="Chat",
    )

    chat_user = ForeignKey(
        "ConferenceFreeParticipant",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="chat_user",
        verbose_name="Darmowy użytkownik",
    )

    status = CharField(
        "Status wiadomości", max_length=32, choices=MODEL_CHAT_MESSAGE_STATUS
    )

    message = TextField(verbose_name="Treść wiadomości", max_length=500)

    approved = BooleanField("Zaakceptowany", default=False)
    approved_at = DateTimeField(
        auto_now_add=True, verbose_name="Data zaakceptowania wiadomości"
    )
    is_aggressor = BooleanField("Zaakceptowany", default=False)
    perspective_score = PositiveSmallIntegerField("Ocena perspektywy", default=0)

    class Meta:
        """Meta"""

        verbose_name = "Wiadomość na chacie"
        verbose_name_plural = "Wiadomości na chacie"
        ordering = ["created_at"]

    def __str__(self):
        return f"Wiadomość od {self.chat_user} w chacie ID: {self.chat}"
