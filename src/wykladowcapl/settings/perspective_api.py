import os

from dotenv import load_dotenv

load_dotenv(override=True)

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
