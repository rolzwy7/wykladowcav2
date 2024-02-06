import os

from dotenv import load_dotenv

load_dotenv(override=True)

MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
