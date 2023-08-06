from django.conf import settings
from pymongo import MongoClient
from pymongo.database import Database

CONNECTION_STRING = (
    "mongodb://{user}:{password}@{host}:{port}/{db_name}".format(
        **{
            "host": settings.MONGO_HOST,
            "port": settings.MONGO_PORT,
            "db_name": settings.MONGO_DB_NAME,
            "user": settings.MONGO_USER,
            "password": settings.MONGO_PASSWORD,
        }
    )
)


def get_mongo_connection() -> tuple[MongoClient, Database]:
    """Return new mongo client and database handle"""
    mongo_client = MongoClient(CONNECTION_STRING)
    database = mongo_client.get_database()
    return mongo_client, database
