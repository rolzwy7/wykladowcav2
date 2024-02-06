import os

from dotenv import load_dotenv

load_dotenv(override=True)

TELEGRAM_API_BASE = "https://api.telegram.org"
TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")
