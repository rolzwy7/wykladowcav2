import os

from dotenv import load_dotenv

load_dotenv(override=True)

JUST_SEND_API_URL = os.environ.get("JUST_SEND_API_URL")
JUST_SEND_API_KEY = os.environ.get("JUST_SEND_API_KEY")
