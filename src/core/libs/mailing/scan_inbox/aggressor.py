"""Scan Inbox - Aggressor"""

# flake8: noqa=E501

from core.consts.aggressor_phrases import AGGRESSOR_PHRASES_ICONTAINS
from core.consts.telegram_chats_consts import TelegramChats
from core.services import BlacklistService
from core.services.telegram_service import TelegramService

from .subject_emails import get_email_subject_emails


def is_email_aggressor(email_subject: str, email_text: str) -> bool:
    """Detect if email is aggressor"""

    for phrase in AGGRESSOR_PHRASES_ICONTAINS:
        if any(
            [
                phrase.lower() in email_subject.lower(),
                phrase.lower() in email_text.lower(),
            ]
        ):
            return True
    return False


def aggressor_phrase_context(text: str, target_phrase: str, char_window=30):
    """aggressor_phrase_context"""
    match_pos = text.lower().find(target_phrase.lower())
    if match_pos == -1:
        return ""
    end_pos = match_pos + len(target_phrase)
    return text[max(0, match_pos - char_window) : min(len(text), end_pos + char_window)]


def aggressor_action(email_from: str, email_subject: str, email_text: str):
    """Action that will be taken when aggressor is detected"""

    # Block temporarily aggressor e-mails
    subject_emails = get_email_subject_emails(email_subject)
    blocked_emails: list[str] = [email_from, *subject_emails]
    for tb_email in blocked_emails:
        BlacklistService.blacklist_email_temporarily(tb_email, days=14)

    # Get contexts of aggressor phrases
    phrases_context_list = []
    for phrase in AGGRESSOR_PHRASES_ICONTAINS:
        aggressor_ctx = aggressor_phrase_context(email_text, phrase)
        if aggressor_ctx:
            phrases_context_list.append(aggressor_ctx)

    return blocked_emails, phrases_context_list


def aggressor_notify(blocked_emails: list[str], phrases_context_list: list[str]):
    """Notify about aggressor detection"""

    telegram_service = TelegramService()
    telegram_service.try_send_chat_message(
        "\n".join(
            [
                "👿 [AGGRESSOR DETECTION] Tymczasowo (14 dni) zablokowano:",
                " ".join(blocked_emails),
                "\nPonieważ wykryto:\n",
                "\n".join(phrases_context_list),
            ]
        ),
        TelegramChats.DEBUG,
    )
