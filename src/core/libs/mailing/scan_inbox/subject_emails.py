"""Scan Inbox - Subject e-mails"""

import re

EMAIL_REGEXP = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"


def get_email_subject_emails(subject: str) -> list[str]:
    """Get emails from e-mail's subject"""
    return list(set(re.findall(EMAIL_REGEXP, subject)))
