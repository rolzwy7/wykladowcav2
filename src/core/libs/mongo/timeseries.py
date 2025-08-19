# -*- coding: utf-8 -*-

# =================================================================
# Funkcje Python do obsługi kolekcji Time-Series w MongoDB
# =================================================================
#
# Autor: Gemini
# Data: 13.08.2025
#
# Opis:
# Zestaw funkcji do interakcji z kolekcją 'events' w MongoDB.
# Umożliwia wstawianie (z opcją sprawdzania zmian), usuwanie oraz
# pobieranie surowych i zagregowanych danych w formacie dla Chart.js.
#
# Wymagania:
# Należy zainstalować biblioteki:
# pip install pymongo
#

# flake8: noqa=E501

from datetime import datetime
from typing import Any, Dict, Literal, Optional

import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure

# Definicja typów dla agregacji
AggregationType = Literal["avg", "sum", "min", "max"]
AggregationPeriod = Literal["day", "month", "year"]


def get_collection(
    connection_string: str,
    db_name: str = "timeseriesDB",
    collection_name: str = "events",
) -> Collection:
    """
    Nawiązuje połączenie z MongoDB i zwraca obiekt kolekcji.

    :param connection_string: Pełny string połączeniowy do MongoDB.
    :param db_name: Nazwa bazy danych.
    :param collection_name: Nazwa kolekcji.
    :return: Obiekt kolekcji MongoDB.
    """
    try:
        client: MongoClient = MongoClient(connection_string)
        # Sprawdzenie połączenia
        client.server_info()
        db = client[db_name]
        collection: Collection = db[collection_name]
        print(
            f"Pomyślnie połączono z bazą danych '{db_name}' i kolekcją '{collection_name}'."
        )
        return collection
    except ConnectionFailure as e:
        print(f"Błąd połączeConnectionFailurenia z MongoDB: {e}")
        raise


def insert_event(
    collection: Collection,
    event_type: str,
    source: str,
    data: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None,
    check_for_change: bool = False,
) -> Optional[ObjectId]:
    """
    Wstawia pojedyncze zdarzenie, z opcją pominięcia, jeśli wartość się nie zmieniła.

    :param collection: Obiekt kolekcji MongoDB.
    :param event_type: Typ zdarzenia.
    :param source: Źródło zdarzenia.
    :param data: Dane specyficzne dla zdarzenia.
    :param metadata: Metadane.
    :param check_for_change: Jeśli True, zdarzenie nie zostanie dodane,
                             jeśli ostatni zapisany rekord ma identyczne pole 'data'.
    :return: ID wstawionego dokumentu lub None, jeśli pominięto.
    """
    if check_for_change:
        last_event = collection.find_one(
            {"eventType": event_type, "source": source},
            sort=[("timestamp", pymongo.DESCENDING)],
        )
        if last_event and last_event.get("data") == data:
            print(
                f"Wartość dla '{event_type}' z '{source}' nie zmieniła się. Pomijam wstawianie."
            )
            return None

    document: Dict[str, Any] = {
        "timestamp": datetime.utcnow(),
        "eventType": event_type,
        "source": source,
        "data": data,
    }
    if metadata:
        document["metadata"] = metadata

    result = collection.insert_one(document)
    print(f"Wstawiono zdarzenie o ID: {result.inserted_id}")
    return result.inserted_id


def delete_events(collection: Collection, filter_query: Dict[str, Any]) -> int:
    """
    Usuwa dokumenty z kolekcji na podstawie podanego filtra.
    """
    result = collection.delete_many(filter_query)
    print(f"Usunięto {result.deleted_count} dokumentów.")
    return result.deleted_count


def get_raw_data_for_chartjs(
    collection: Collection,
    event_type: str,
    source: str,
    start_date: datetime,
    end_date: datetime,
    data_field: str,
) -> Dict[str, Any]:
    """
    Pobiera surowe (niezagregowane) dane z podanego okresu.

    :return: Słownik z danymi gotowy do przekazania do Chart.js.
    """
    query = {
        "eventType": event_type,
        "source": source,
        "timestamp": {"$gte": start_date, "$lte": end_date},
        f"data.{data_field}": {"$exists": True},
    }

    cursor = collection.find(query).sort("timestamp", 1)

    labels: list[str] = []
    data_points: list[Any] = []
    for doc in cursor:
        labels.append(doc["timestamp"].strftime("%Y-%m-%d %H:%M:%S"))
        data_points.append(doc["data"].get(data_field))

    return {
        "labels": labels,
        "datasets": [
            {
                "label": f"Wartość {data_field}",
                "data": data_points,
                "borderColor": "rgb(75, 192, 192)",
                "tension": 0.1,
            }
        ],
    }


def get_aggregated_data_for_chartjs(
    collection: Collection,
    event_type: str,
    source: str,
    start_date: datetime,
    end_date: datetime,
    data_field: str,
    aggregation_type: AggregationType = "avg",
    aggregation_period: AggregationPeriod = "day",
) -> Dict[str, Any]:
    """
    Pobiera i agreguje dane w podanych okresach (dzień, miesiąc, rok).

    :param aggregation_type: Typ agregacji: 'avg', 'sum', 'min', 'max'.
    :param aggregation_period: Okres agregacji: 'day', 'month', lub 'year'.
    :return: Słownik z danymi gotowy do przekazania do Chart.js.
    """
    if aggregation_period not in ["day", "month", "year"]:
        raise ValueError("aggregation_period musi być 'day', 'month' lub 'year'")
    if aggregation_type not in ["avg", "sum", "min", "max"]:
        raise ValueError("aggregation_type musi być 'avg', 'sum', 'min' lub 'max'")

    group_id_format: Dict[str, Any] = {
        "day": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
        "month": {"$dateToString": {"format": "%Y-%m", "date": "$timestamp"}},
        "year": {"$dateToString": {"format": "%Y", "date": "$timestamp"}},
    }

    aggregation_operator = {f"${aggregation_type}": f"$data.{data_field}"}

    pipeline: list[Dict[str, Any]] = [
        {
            "$match": {
                "eventType": event_type,
                "source": source,
                "timestamp": {"$gte": start_date, "$lte": end_date},
                f"data.{data_field}": {
                    "$exists": True,
                    "$type": "number",
                },  # Agregacja tylko na liczbach
            }
        },
        {
            "$group": {
                "_id": group_id_format[aggregation_period],
                "value": aggregation_operator,
            }
        },
        {"$sort": {"_id": 1}},
    ]

    cursor = collection.aggregate(pipeline)

    labels: list[str] = []
    data_points: list[Optional[float]] = []
    for doc in cursor:
        labels.append(doc["_id"])
        data_points.append(round(doc["value"], 2))

    aggregation_labels = {
        "avg": "Średnia",
        "sum": "Suma",
        "min": "Minimum",
        "max": "Maksimum",
    }

    return {
        "labels": labels,
        "datasets": [
            {
                "label": f"{aggregation_labels[aggregation_type]} {data_field} ({aggregation_period})",
                "data": data_points,
                "borderColor": "rgb(255, 99, 132)",
                "backgroundColor": "rgba(255, 99, 132, 0.5)",
            }
        ],
    }


# # --- PRZYKŁAD UŻYCIA ---
# if __name__ == "__main__":
#     MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"

#     try:
#         events_collection = get_collection(MONGO_CONNECTION_STRING)

#         # Czyszczenie starych danych testowych
#         delete_events(events_collection, {"source": "server_1"})

#         # Wstawienie danych do agregacji
#         print("\n--- Wstawianie danych do agregacji ---")
#         events_collection.insert_one(
#             {
#                 "timestamp": datetime(2025, 8, 10, 10, 0),
#                 "eventType": "cpu_load",
#                 "source": "server_1",
#                 "data": {"load": 50},
#             }
#         )
#         events_collection.insert_one(
#             {
#                 "timestamp": datetime(2025, 8, 10, 12, 0),
#                 "eventType": "cpu_load",
#                 "source": "server_1",
#                 "data": {"load": 60},
#             }
#         )
#         events_collection.insert_one(
#             {
#                 "timestamp": datetime(2025, 8, 11, 10, 0),
#                 "eventType": "cpu_load",
#                 "source": "server_1",
#                 "data": {"load": 40},
#             }
#         )
#         events_collection.insert_one(
#             {
#                 "timestamp": datetime(2025, 8, 11, 14, 0),
#                 "eventType": "cpu_load",
#                 "source": "server_1",
#                 "data": {"load": 45},
#             }
#         )

#         start_date = datetime(2025, 8, 1)
#         end_date = datetime(2025, 8, 31)

#         # 1. Pobieranie surowych danych
#         print("\n--- Pobieranie surowych danych ---")
#         raw_data = get_raw_data_for_chartjs(
#             collection=events_collection,
#             event_type="cpu_load",
#             source="server_1",
#             start_date=start_date,
#             end_date=end_date,
#             data_field="load",
#         )
#         print("Surowe obciążenie CPU:")
#         print(json.dumps(raw_data, indent=4))

#         # 2. Pobieranie danych zagregowanych (różne typy)
#         print("\n--- Pobieranie danych zagregowanych (dziennie) ---")

#         # Średnia
#         avg_data = get_aggregated_data_for_chartjs(
#             collection=events_collection,
#             event_type="cpu_load",
#             source="server_1",
#             start_date=start_date,
#             end_date=end_date,
#             data_field="load",
#             aggregation_type="avg",
#         )
#         print("\nŚrednie dzienne obciążenie CPU:")
#         print(json.dumps(avg_data, indent=4))

#         # Suma
#         sum_data = get_aggregated_data_for_chartjs(
#             collection=events_collection,
#             event_type="cpu_load",
#             source="server_1",
#             start_date=start_date,
#             end_date=end_date,
#             data_field="load",
#             aggregation_type="sum",
#         )
#         print("\nSuma dzienna obciążenia CPU:")
#         print(json.dumps(sum_data, indent=4))

#         # Maksimum
#         max_data = get_aggregated_data_for_chartjs(
#             collection=events_collection,
#             event_type="cpu_load",
#             source="server_1",
#             start_date=start_date,
#             end_date=end_date,
#             data_field="load",
#             aggregation_type="max",
#         )
#         print("\nMaksymalne dzienne obciążenie CPU:")
#         print(json.dumps(max_data, indent=4))

#     except ConnectionFailure:
#         print(
#             "\nNie udało się połączyć z bazą danych. Upewnij się, że MongoDB jest uruchomione."
#         )
#     except Exception as e:
#         print(f"Wystąpił nieoczekiwany błąd: {e}")
