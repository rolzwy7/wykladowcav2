"""Scan Inbox - Bounces"""

from email.message import Message

from flufl.bounce import all_failures


def get_emails_permanent_failures(message: Message):
    """Get permanent failures (emails) from message"""
    _, permanent = all_failures(message)
    return [str(_, "utf8").lower() for _ in permanent]


def get_emails_temporary_failures(message: Message):
    """Get temporary failures (emails) from message"""
    temporary, _ = all_failures(message)
    return [str(_, "utf8").lower() for _ in temporary]


def is_bounce_by_subject(email_subject: str) -> bool:
    """Check if email message's subject indicate bounce"""

    phrases = [
        "failure notice",
        "undeliverable",
        "undelivered",
        "delivery failed",
        "returned mail",
    ]
    for phrase in phrases:
        if phrase.lower() in email_subject.lower():
            return True
    return False
