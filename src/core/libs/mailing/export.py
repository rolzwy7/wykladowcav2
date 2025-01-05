"""Export emails"""

# flake8: noqa=E501

from django.db.models import Q

from core.libs.mongo.db import get_dwpldbv3_connection, get_mongo_connection
from core.models import Lecturer, WebinarParticipant
from core.models.conference import ConferenceFreeParticipant
from core.models.enums import WebinarStatus


def export_emails_campaign_clicks(campaign_id: int) -> list[str]:
    """export_emails_campaign_clicks"""

    client, db = get_mongo_connection()

    # Find all clicks
    tracking_codes = [
        doc["tracking_code"]
        for doc in db["wykladowcav2_mailing_clicks"].find(
            {"campaign_id": campaign_id}, {"tracking_code": 1, "_id": 0}
        )
    ]

    # Get e-mail by tracking codes
    emails: list[str] = [
        doc["email"]
        for doc in db["wykladowcav2_mailing_tracking"].find(
            {"_id": {"$in": tracking_codes}}, {"email": 1, "_id": 0}
        )
    ]

    client.close()

    return emails


def export_emails_lecturer_done_webinars(lecturer_id: int) -> list[str]:
    """export_emails_lecturer_done_webinars"""
    lecturer = Lecturer.manager.get(id=lecturer_id)
    pairticipants = WebinarParticipant.manager.filter(
        Q(application__webinar__lecturer=lecturer)
        & Q(application__webinar__status=WebinarStatus.DONE)
    )
    return list(set([_.email for _ in pairticipants]))


def export_emails_lecturer_all_webinars(lecturer_id: int) -> list[str]:
    """export_emails_lecturer_all_webinars"""

    lecturer = Lecturer.manager.get(id=lecturer_id)
    pairticipants = WebinarParticipant.manager.filter(
        application__webinar__lecturer=lecturer
    )
    return list(set([_.email for _ in pairticipants]))


def export_emails_lecturer_participants_free(lecturer_id: int) -> list[str]:
    """export_emails_lecturer_all_webinars"""
    lecturer = Lecturer.manager.get(id=lecturer_id)

    pairticipants = ConferenceFreeParticipant.manager.filter(
        edition__webinar__lecturer=lecturer
    )
    return list(set([_.email for _ in pairticipants]))


def export_emails_mongo_tagged(tag: str) -> list[str]:
    """export_emails_mongo_tagged"""

    client, db = get_dwpldbv3_connection()
    emails = [
        doc["email"]
        for doc in db["mailing_database"].find({"tag": tag}, {"email": 1, "_id": 0})
    ]
    client.close()

    return list(set(emails))


def export_emails_mongo_index_tags() -> list[tuple[str, str]]:
    """export_emails_mongo_index_tags"""

    client, db = get_dwpldbv3_connection()
    tags_index = [
        (doc["_id"], doc["count"]) for doc in db["mailing_database_index"].find({})
    ]
    client.close()

    return tags_index
