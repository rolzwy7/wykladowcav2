import os

from dotenv import load_dotenv

load_dotenv(override=True)

NIEBIESKI_ZAPYTANIE_LOGIN = os.environ.get("NIEBIESKI_ZAPYTANIE_LOGIN")
NIEBIESKI_ZAPYTANIE_PASSWORD = os.environ.get("NIEBIESKI_ZAPYTANIE_PASSWORD")
