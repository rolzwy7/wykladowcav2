"""Scan Inbox - New E-mail"""


def is_new_email(email_subject: str, email_text: str) -> bool:
    """Does e-mail message advertisies new email"""

    # Check if subject contains words indicating vacation
    phrases = [
        "zmiana konta pocztowego",
        "nowy mail",
        "nowy email",
        "nowy e-mail",
        "nowe adres",
        "nowy adres",
    ]
    for phrase in phrases:
        if any(
            [
                phrase.lower() in email_subject.lower(),
                phrase.lower() in email_text.lower(),
            ]
        ):
            return True
    return False
