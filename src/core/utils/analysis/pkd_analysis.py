"""PKD analysis"""

# flake8: noqa=E501

from django.db.models import QuerySet

from core.libs.mongo.db import get_dwpldbv3_connection
from core.models.webinar_application_model import WebinarApplication


def analyse_pkd_for_applications(applications: QuerySet[WebinarApplication]):
    """Get PKD analysis for given applications"""

    # Get NIPs and NIP types
    nips = []
    nip_type_map: dict[str, str] = {}
    for application in applications:
        if application.buyer:
            nips.append(application.buyer.nip)
            nip_type_map[application.buyer.nip] = "Nabywca"
        if application.recipient:
            nips.append(application.recipient.nip)
            nip_type_map[application.recipient.nip] = "Odbiorca"

    client, db = get_dwpldbv3_connection()

    # Get PKDs for NIP numbers
    pkds = []
    nip_pkds_map: dict[str, list[str]] = {}
    pkd_main_map: dict[str, bool] = {}
    for document in db["regon_prawna_pkds"].find({"nip": {"$in": nips}}):
        nip = document["nip"]
        pkd = document["pkd"]
        pkds.append(pkd)
        pkd_main_map[pkd] = document["main"]
        if nip in nip_pkds_map:
            nip_pkds_map[nip].append(pkd)
        else:
            nip_pkds_map[nip] = [pkd]

    # Get name for pkds
    pkd_name_map: dict[str, str] = {}
    for pkd in pkds:
        document = db["consts_pkd"].find_one({"_id": pkd})
        if document:
            pkd_name_map[pkd] = document["nazwa"]

    client.close()

    return [
        (
            nip,
            nip_type_map[nip],
            [
                (
                    pkd_main_map[pkd],
                    pkd,
                    pkd_name_map.get(pkd, "brak opisu numeru PKD w bazie"),
                )
                for pkd in nip_pkds_map.get(nip, [])
            ],
        )
        for nip in nips
    ]
