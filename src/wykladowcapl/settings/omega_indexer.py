import os

from dotenv import load_dotenv

load_dotenv(override=True)

OMEGA_INDEXER_API_KEY = os.environ.get("OMEGA_INDEXER_API_KEY")
