"""dev_command"""

# flake8: noqa=E501
import json
from pprint import pprint
from random import choice, shuffle
from string import ascii_uppercase, digits

import mysql.connector
import requests
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils.timezone import datetime
from openai.types.chat import ChatCompletion
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.libs.konkurencja.centrum_verte import CentrumVerteFetcher
from core.libs.konkurencja.flightcontrol import konkurencja_fetcher
from core.libs.mongo import timeseries
from core.libs.mongo.db import get_mongo_connection
from core.libs.openai import get_completion_usage, get_openapi_client, openai_completion
from core.libs.openai.system_prompts import (
    SYSPROMPT_TEXT2TEXT_KONKURENCJA_PROGRAM_PARAFRAZA,
)
from core.models import WebinarAggregate


class Command(BaseCommand):
    """dev_command"""

    help = "dev_command"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        # Connect to server
        cnx = mysql.connector.connect(
            host="mysql28.mydevil.net",
            port=3306,
            user="m1431_eventis",
            password="z74xCu16O6SaNGVp",
            database="m1431_eventis",
        )

        # Get a cursor
        cur = cnx.cursor()

        print("Executing query")

        # Execute a query
        cur.execute("SELECT * FROM szkolenia")

        # Fetch one result
        print("Fetching ...")
        row = cur.fetchone()
        while row:
            print(row[0])

            url = row[1]
            title = row[2]
            print(title)

            program_html = row[5]

            oa_client = get_openapi_client()

            messages = []

            messages.append(
                {
                    "role": "system",
                    "content": SYSPROMPT_TEXT2TEXT_KONKURENCJA_PROGRAM_PARAFRAZA,
                }
            )

            messages.append({"role": "user", "content": program_html})

            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "set_program_html",
                        "parameters": {
                            "type": "object",
                            "properties": {"html": {"type": "string"}},
                            "required": ["html"],
                        },
                    },
                }
            ]

            completion: ChatCompletion = oa_client.chat.completions.create(
                model="gpt-4o-mini", messages=messages, tools=tools, tool_choice="auto"
            )

            response = completion.choices[0].message.content
            tool = completion.choices[0].message.tool_calls[0]
            args = json.loads(tool.function.arguments)

            usage = get_completion_usage(completion)
            if usage:
                print(usage.dict())
            else:
                print("NO USAGE")

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

            save_program_html = ""
            save_program_html += f'<a href={url} target="_blank">{url}</a>'
            save_program_html += "<hr/>"
            save_program_html += args["html"]

            aggregate = WebinarAggregate(
                pod_szkolenie_zamkniete=True,
                hidden=True,
                program=save_program_html,
                grouping_token=candid_grouping_token,
                slug=slugify(title),
                title=title,
            )
            aggregate.save()

            row = cur.fetchone()

        # Close connections
        cnx.close()


# class Command(BaseCommand):
#     """dev_command"""

#     help = "dev_command"

#     def add_arguments(self, parser):
#         pass

#     def handle(self, *args, **options):

#         client, db = get_mongo_connection()
#         collection = db["wykladowcav2_timeseries"]

#         timeseries.insert_event(
#             collection, "event_type", "source", {"count": 456}, check_for_change=True
#         )
#         start_date = datetime(2025, 8, 1)
#         end_date = datetime(2025, 8, 31)
#         ret = timeseries.get_raw_data_for_chartjs(
#             collection,
#             "event_type",
#             "source",
#             start_date=start_date,
#             end_date=end_date,
#             data_field="count",
#         )
#         print(ret)


# class Command(BaseCommand):
#     """dev_command"""

#     help = "dev_command"

#     def add_arguments(self, parser):
#         pass

#     def handle(self, *args, **options):
#         url = "https://centrumverte.pl/szkolenia-online/likwidacja-majatku-trwalego-w-jednostkach-budzetowych-zmiany-od-grudnia-2023r-warsztaty-praktyczne-szkolenie-online/"
#         url = "https://www.jgt.pl/szkolenia,transgraniczne-przemieszczanie-odpadow-tgs.html"
#         url = "https://izbapodatkowa.pl/szkolenie/transakcje-z-podmiotami-powiazanymi-a-podatki-dochodowe-preferencje-obostrzenia-i-zagrozenia/?termin=21468"
#         fetcher = konkurencja_fetcher(url)

#         print("=" * 32)
#         print("get_program:", fetcher.get_program())
#         print("get_lecturer:", fetcher.get_lecturer())
#         print("get_price:", fetcher.get_price())
#         print("get_date:", fetcher.get_date())
#         print("get_title:", fetcher.get_title())
#         print("=" * 32)
#         pprint(fetcher.logs)
