class ChatMessageStatusEnum:
    """ChatMessageStatusEnum"""

    INIT = "INIT"
    MANUAL_ADMIN = "MANUAL_ADMIN"
    AGGRESSOR = "AGGRESSOR"
    AUTO_ADMIN = "AUTO_ADMIN"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


MODEL_CHAT_MESSAGE_STATUS = [
    (ChatMessageStatusEnum.INIT, "Wstępne przetwarzanie wiadomości"),
    (ChatMessageStatusEnum.MANUAL_ADMIN, "Ręczna administracja"),
    (ChatMessageStatusEnum.AGGRESSOR, "Agresor zbanowany automatycznie"),
    (ChatMessageStatusEnum.AUTO_ADMIN, "Automatyczna administracja (algorytm)"),
    (ChatMessageStatusEnum.ACCEPTED, "Wiadomość zaakceptowana"),
    (ChatMessageStatusEnum.REJECTED, "Wiadomość odrzucona"),
]
