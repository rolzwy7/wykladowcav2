import os

from dotenv import load_dotenv

load_dotenv(override=True)

OPENAPI_API_KEY = os.environ.get("OPENAPI_API_KEY")
