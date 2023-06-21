import os

from dotenv import load_dotenv

load_dotenv()

# Base URL for ClickMeeting
CLICKMEETING_API_URL = "https://api.clickmeeting.com/v1"

CLICKMEETING_API_KEY = os.environ.get("CLICKMEETING_API_KEY")  # Secret
