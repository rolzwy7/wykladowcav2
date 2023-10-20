from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from core.libs.mongo.db import get_mongo_connection


@cache_page(30)
def crm_resignations_plaintext(request):
    """CRM resignations plaintext"""

    client, database = get_mongo_connection()
    query = database.wykladowcav2_mailing_resignations.find({"confirmed": True})
    emails = [record["email"] for record in query]
    client.close()

    emails = list(sorted(emails))

    return HttpResponse("\n".join(emails), content_type="text/plain")
