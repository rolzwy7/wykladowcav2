import os

from dotenv import load_dotenv

load_dotenv(override=True)

# Base URL for ClickMeeting
CLICKMEETING_API_URL = "https://api.clickmeeting.com/v1"

CLICKMEETING_DOMAIN = "https://wykladowcapl.clickmeeting.com"

CLICKMEETING_API_KEY = os.environ.get("CLICKMEETING_API_KEY")  # Secret
