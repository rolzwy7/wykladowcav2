"""dev_command"""

# flake8: noqa=E501
from pprint import pprint

import requests
from django.core.management.base import BaseCommand

from core.libs.konkurencja.centrum_verte import CentrumVerteFetcher
from core.libs.konkurencja.flightcontrol import konkurencja_fetcher


class Command(BaseCommand):
    """dev_command"""

    help = "dev_command"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        url = "https://centrumverte.pl/szkolenia-online/likwidacja-majatku-trwalego-w-jednostkach-budzetowych-zmiany-od-grudnia-2023r-warsztaty-praktyczne-szkolenie-online/"
        url = "https://www.jgt.pl/szkolenia,transgraniczne-przemieszczanie-odpadow-tgs.html"
        url = "https://izbapodatkowa.pl/szkolenie/transakcje-z-podmiotami-powiazanymi-a-podatki-dochodowe-preferencje-obostrzenia-i-zagrozenia/?termin=21468"
        fetcher = konkurencja_fetcher(url)

        print("=" * 32)
        print("get_program:", fetcher.get_program())
        print("get_lecturer:", fetcher.get_lecturer())
        print("get_price:", fetcher.get_price())
        print("get_date:", fetcher.get_date())
        print("get_title:", fetcher.get_title())
        print("=" * 32)
        pprint(fetcher.logs)
