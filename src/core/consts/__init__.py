# flake8: noqa
from .email_dangerous_phrases import DANGEROUSE_PHRASES
from .exemptions_consts import (
    ALLOWED_EXEMPTIONS_BY_APPLICATION_TYPE,
    CHOICES_VAT_EXEMPTIONS,
    PRICE_ADNOTATION,
    TAX_EXEMPT_TOOLTIP,
    VAT_EXEMPTION_0,
    VAT_EXEMPTION_13,
    VAT_EXEMPTION_36,
    VAT_EXEMPTION_113,
    VAT_EXEMPTIONS,
    VAT_VALUE_PERCENT,
    WE_ARE_TAX_EXEMPT,
)
from .patron_consts import (
    PATRON_EMAIL,
    PATRON_FIRST_NAME,
    PATRON_JOB_TITLE,
    PATRON_LAST_NAME,
    PATRON_PHONE,
)
from .requests_consts import GET, POST
from .slugs_consts import SLUG_HELP_TEXT
from .tagging_consts import INIT_TAGS
from .telegram_chats_consts import TelegramChats
from .webmail_consts import WEBMAILS
