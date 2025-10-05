# flake8: noqa:E501
# pylint: disable=line-too-long


class MailingScheduledStatus:
    """Represents status of mailing schedule"""

    INIT = "INIT"
    SCHEDULED = "SCHEDULED"
    CANCELED = "CANCELED"


class MailingCampaignStatus:
    """Represents status of mailing campaign"""

    PAUSED = "PAUSED"
    SENDING = "SENDING"
    DONE = "DONE"


class MailingCampaignWarmupStatus:
    """Represents status of mailing warmup"""

    NO_WARMUP = "NO_WARMUP"
    WARMUP_ACTIVE = "WARMUP_ACTIVE"
    WARMUP_FINISHED = "WARMUP_FINISHED"


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

    # Resignation
    RESIGNATION = "RESIGNATION"

    # Not email
    INVALID_EMAIL_FORMAT = "INVALID_EMAIL_FORMAT"

    # Unexpected error
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"

    # Connection error
    SMTP_SERVER_DISCONNECTED = "SMTP_SERVER_DISCONNECTED"
    CONNECTION_REFUSED = "CONNECTION_REFUSED"
    RECIPIENT_REFUSED = "RECIPIENT_REFUSED"

    # Is customer
    IS_ALREADY_CUSTOMER = "IS_ALREADY_CUSTOMER"

    # Was already sent today to given email
    ALREADY_SENT_TODAY = "ALREADY_SENT_TODAY"

    # Success status
    SENT = "SENT"


mailing_pool_status_display_map = {
    MailingPoolStatus.BEING_PROCESSED: "W trakcie przetwarzania",
    MailingPoolStatus.READY_TO_SEND: "Gotowe do wysyłki",
    MailingPoolStatus.MX_INVALID: "MX niepoprawny",
    MailingPoolStatus.MX_VALID: "MX poprawny",
    MailingPoolStatus.DANGEROUS_TO_SEND: "Niebezpieczny",
    MailingPoolStatus.VACATION: "Wakacje",
    MailingPoolStatus.RESIGNATION: "Rezygnacja",
    MailingPoolStatus.BLACKLISTED_PREFIX: "Zablokowany prefix",
    MailingPoolStatus.BLACKLISTED_DOMAIN: "Zablokowana domena",
    MailingPoolStatus.BLACKLISTED_EMAIL: "Zablokowany e-mail",
    MailingPoolStatus.BLACKLISTED_EMAIL_TEMPORARY: "Zablokowano e-mail (tymczasowo)",
    MailingPoolStatus.BLACKLISTED_PHRASE: "Zablokowana fraza",
    MailingPoolStatus.BOUNCE_UNKNOWN: "Odbicie (unknown)",
    MailingPoolStatus.BOUNCE_PERMANENT: "Odbicie twarde",
    MailingPoolStatus.BOUNCE_TEMPORARY: "Odbicie miękkie",
    MailingPoolStatus.INVALID_EMAIL_FORMAT: "Niepoprawny format e-mail",
    MailingPoolStatus.IS_ALREADY_CUSTOMER: "JUŻ BYŁ KLIENTEM AGREGATU",
    MailingPoolStatus.ALREADY_SENT_TODAY: "WYSŁANO DZIŚ JUŻ DO TEGO ADRESU E-MAIL",
    MailingPoolStatus.UNEXPECTED_ERROR: "UNEXPECTED_ERROR",
    MailingPoolStatus.SENT: "Wysłano",
    MailingPoolStatus.SMTP_SERVER_DISCONNECTED: "ERROR SMTP_SERVER_DISCONNECTED",
    MailingPoolStatus.CONNECTION_REFUSED: "ERROR CONNECTION_REFUSED",
    MailingPoolStatus.RECIPIENT_REFUSED: "ERROR RECIPIENT_REFUSED",
}
