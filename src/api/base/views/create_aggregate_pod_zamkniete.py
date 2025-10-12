"""
create_aggregate_pod_zamkniete
"""

from random import choice, shuffle
from string import ascii_uppercase, digits

from django.utils.text import slugify
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import WebinarAggregate


@api_view(["POST"])
def create_aggregate_pod_zamkniete(request):
    """
    create_aggregate_pod_zamkniete
    """

    title = request.data["title"]
    program_html = request.data["program_html"]

    # Generate grouping token
    random_base = list(f"{ascii_uppercase}{digits}")
    shuffle(random_base)

    for _ in range(1_000):
        candid_grouping_token = "ZAMK-" + "".join(
            [choice(random_base) for _ in range(8)]
        )
        if WebinarAggregate.manager.filter(
            grouping_token=candid_grouping_token
        ).exists():
            continue
        break

    aggregate = WebinarAggregate(
        pod_szkolenie_zamkniete=True,
        hidden=True,
        program=program_html,
        grouping_token=candid_grouping_token,
        slug=slugify(title),
        title=title,
    )
    aggregate.save()

    return Response(
        {"status": "ok"},
        status=status.HTTP_200_OK,
    )
