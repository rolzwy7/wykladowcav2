import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_BASE = "https://api.telegram.org"
TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")
TELEGRAM_CHAT_ID_APPLICATIONS = "-439442270"
TELEGRAM_CHAT_ID_OTHER = "-408682505"
