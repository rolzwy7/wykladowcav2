"""mongo db connection"""

# flake8: noqa=E501

from urllib.parse import quote_plus

from django.conf import settings
from pymongo import MongoClient
from pymongo.database import Database

CONNECTION_STRING = "mongodb://{user}:{password}@{host}:{port}/{db_name}".format(
    **{
        "host": settings.MONGO_HOST,
        "port": settings.MONGO_PORT,
        "db_name": settings.MONGO_DB_NAME,
        "user": quote_plus(settings.MONGO_USER),
        "password": quote_plus(settings.MONGO_PASSWORD),
    }
)


class MongoDBClient:
    """MongoDBClient"""

    _client = None

    @staticmethod
    def get_connection():
        """get_connection"""
        if MongoDBClient._client is None:
            # Replace with your MongoDB URI and options
            MongoDBClient._client = MongoClient(CONNECTION_STRING)

        return MongoDBClient._client, MongoDBClient._client.get_database()


def get_mongo_connection() -> tuple[MongoClient, Database]:
    """Return new mongo client and database handle"""
    mongo_client = MongoClient(CONNECTION_STRING)
    database = mongo_client.get_database()
    return mongo_client, database


def get_dwpldbv3_connection() -> tuple[MongoClient, Database]:
    """get_dwpldbv3_connection"""
    conn_str = "mongodb://{user}:{password}@{host}:{port}/{db_name}".format(
        **{
            "host": settings.DWPLDBV3_HOST,
            "port": settings.DWPLDBV3_PORT,
            "db_name": settings.DWPLDBV3_DB_NAME,
            "user": quote_plus(settings.DWPLDBV3_USER),
            "password": quote_plus(settings.DWPLDBV3_PASSWORD),
        }
    )
    mongo_client = MongoClient(conn_str)
    database = mongo_client.get_database()
    return mongo_client, database
