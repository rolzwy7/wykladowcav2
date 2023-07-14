import os

from dotenv import load_dotenv

load_dotenv()

REDIS_DB = os.environ.get("REDIS_DB", "0")
REDIS_USER = os.environ.get("REDIS_USER")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")  # Secret
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
