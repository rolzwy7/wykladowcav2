import os

from dotenv import load_dotenv

load_dotenv()

FAKTUROWNIA_API_URL = os.environ.get("FAKTUROWNIA_API_URL")
FAKTUROWNIA_API_KEY = os.environ.get("FAKTUROWNIA_API_KEY")
