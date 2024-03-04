"""Settings for celery flower"""

import os

from dotenv import load_dotenv

load_dotenv(override=True)

FLOWER_HOST = os.environ.get("FLOWER_HOST")
FLOWER_PORT = os.environ.get("FLOWER_PORT")
FLOWER_USER = os.environ.get("FLOWER_USER")
FLOWER_PASSWORD = os.environ.get("FLOWER_PASSWORD")
FLOWER_BASE_URL = f"{FLOWER_HOST}:{FLOWER_PORT}"
