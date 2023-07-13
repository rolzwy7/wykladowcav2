import os

from dotenv import load_dotenv

load_dotenv()

# TODO: ING Ksiegowosc - Delete this because we no longer use it

# Base URL for Ing Księgowość API
INGKSIEGOWOSC_API_BASE_URL = "https://ksiegowosc.ing.pl/v2"

INGKSIEGOWOSC_API_KEY = os.environ.get("INGKSIEGOWOSC_API_KEY")  # Secret
