"""Scan Inbox - Vacation"""

# flake8: noqa=E501

from core.consts.telegram_chats_consts import TelegramChats
from core.services import BlacklistService, TelegramService

from .subject_emails import get_email_subject_emails

VACATION_CONTENT_PHRASES = [
    "przebywam na urlopie",
    "jestem na urlopie",
    "mam urlop",
]
VACATION_SUBJECT_PHRASES = [
    "nieobecn",
    "urlop",
    "urlopie",
    "abwesenheit",
    "przebywam na urlopie",
    "nieczynne biuro",
]


def is_email_content_vacation(email_text: str) -> bool:
    """Detect if email's content indicates vaction"""

    for vacation_phrase in VACATION_CONTENT_PHRASES:
        if vacation_phrase.lower() in email_text.lower():
            return True
    return False


def is_email_subject_vacation(email_subject: str) -> bool:
    """Detect if email's subject indicates vaction"""

    for vacation_phrase in VACATION_SUBJECT_PHRASES:
        if vacation_phrase.lower() in email_subject.lower():
            return True
    return False


def vacation_phrase_context(text: str, target_phrase: str, char_window=30):
    """vacation_phrase_context"""
    match_pos = text.lower().find(target_phrase.lower())
    if match_pos == -1:
        return ""
    end_pos = match_pos + len(target_phrase)
    return text[max(0, match_pos - char_window) : min(len(text), end_pos + char_window)]


def vacation_action(email_from: str, email_subject: str, email_text: str):
    """vacation_action"""
    subject_emails = get_email_subject_emails(email_subject)
    blocked_emails = [email_from, *subject_emails]

    # Block temporarily
    for vacation_email in blocked_emails:
        BlacklistService.blacklist_email_temporarily(vacation_email, days=10)

    # Get contexts of vacation phrases in email's content
    phrases_context_list = []
    for phrase in VACATION_CONTENT_PHRASES:
        aggressor_ctx = vacation_phrase_context(email_text, phrase)
        if aggressor_ctx:
            phrases_context_list.append(aggressor_ctx)

    return blocked_emails, phrases_context_list


def vacation_notify(
    email_subject: str,
    blocked_emails: list[str],
    phrases_context_list: list[str],
    is_vacation_subject: bool,
    is_vacation_content: bool,
):
    """vacation_notify"""
    telegram_service = TelegramService()

    msg = []

    if is_vacation_subject:
        msg.append("\nWykryto słowa kluczowe w temacie:")
    else:
        msg.append("\nNie wykryto słów kluczowych w temacie")

    if is_vacation_content:
        msg.append("\nWykryto w treści:")
        msg.append("\n".join(phrases_context_list))
    else:
        msg.append("\nNie wykryto słów kluczowych w treści")

    # telegram_service.try_send_chat_message(
    #     "\n".join(
    #         [
    #             "🏝️ [Urlop] Tymczasowo (10 dni) zablokowano:",
    #             " ".join(blocked_emails),
    #             "\nTytuł wiadomości e-mail:",
    #             email_subject,
    #             *msg,
    #         ]
    #     ),
    #     TelegramChats.DEBUG,
    # )
