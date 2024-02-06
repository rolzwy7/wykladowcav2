import os

from dotenv import load_dotenv

load_dotenv(override=True)

REGON_API_KEY = os.environ.get("REGON_API_KEY")  # Secret
