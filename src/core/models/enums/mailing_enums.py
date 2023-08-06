# flake8: noqa:E501
# pylint: disable=line-too-long


class MailingCampaignStatus:
    """Represents status of mailing campaign"""

    PAUSED = "PAUSED"
    SENDING = "SENDING"
    DONE = "DONE"


class MailingBounceStatus:
    """Represents bounce status"""

    TEMPORARY = "TEMPORARY"
    PERMANENT = "PERMANENT"
    SPAMBLOCK = "SPAMBLOCK"


class MailingPoolStatus:
    """Represents status of mailing pool object"""

    # Init status
    BEING_PROCESSED = "BEING_PROCESSED"
    READY_TO_SEND = "READY_TO_SEND"

    # MX
    MX_INVALID = "MX_INVALID"
    MX_VALID = "MX_VALID"

    # Always dangerous to send e-mails
    DANGEROUS_TO_SEND = "DANGEROUS_TO_SEND"

    # Vacation
    VACATION = "VACATION"

    # Blacklisted
    BLACKLISTED_PREFIX = "BLACKLISTED_PREFIX"
    BLACKLISTED_DOMAIN = "BLACKLISTED_DOMAIN"
    BLACKLISTED_EMAIL = "BLACKLISTED_EMAIL"
    BLACKLISTED_EMAIL_TEMPORARY = "BLACKLISTED_EMAIL_TEMPORARY"
    BLACKLISTED_PHRASE = "BLACKLISTED_PHRASE"

    # Bounce
    BOUNCE_UNKNOWN = "BOUNCE_UNKNOWN"
    BOUNCE_PERMANENT = "BOUNCE_PERMANENT"
    BOUNCE_TEMPORARY = "BOUNCE_TEMPORARY"

    # Not email
    INVALID_EMAIL_FORMAT = "INVALID_EMAIL_FORMAT"

    # Unexpected error
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"

    # Success status
    SENT = "SENT"


mailing_pool_status_display_map = {
    MailingPoolStatus.BEING_PROCESSED: "W trakcie przetwarzania",
    MailingPoolStatus.READY_TO_SEND: "Gotowe do wysyłki",
    MailingPoolStatus.MX_INVALID: "MX niepoprawny",
    MailingPoolStatus.MX_VALID: "MX poprawny",
    MailingPoolStatus.DANGEROUS_TO_SEND: "Niebezpieczny",
    MailingPoolStatus.VACATION: "Wakacje",
    MailingPoolStatus.BLACKLISTED_PREFIX: "Zablokowany prefix",
    MailingPoolStatus.BLACKLISTED_DOMAIN: "Zablokowana domena",
    MailingPoolStatus.BLACKLISTED_EMAIL: "Zablokowany e-mail",
    MailingPoolStatus.BLACKLISTED_EMAIL_TEMPORARY: "Zablokowano e-mail (tymczasowo)",
    MailingPoolStatus.BLACKLISTED_PHRASE: "Zablokowana fraza",
    MailingPoolStatus.BOUNCE_UNKNOWN: "Odbicie (unknown)",
    MailingPoolStatus.BOUNCE_PERMANENT: "Odbicie twarde",
    MailingPoolStatus.BOUNCE_TEMPORARY: "Odbicie miękkie",
    MailingPoolStatus.INVALID_EMAIL_FORMAT: "Niepoprawny format e-mail",
    MailingPoolStatus.UNEXPECTED_ERROR: "UNEXPECTED_ERROR",
    MailingPoolStatus.SENT: "Wysłano",
}
