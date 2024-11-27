"""
Temporary command - fill leads with participants
"""

# flake8: noqa=E501
# pylint: disable=line-too-long

from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from lxml import html
from requests.sessions import Session

from core.consts.telegram_chats_consts import TelegramChats
from core.tasks.send_telegram_notification.procedure import send_telegram_notification

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"


class Command(BaseCommand):
    """temp_cmd_fill_leads"""

    def execute_command(self, alias, base_url, login, password):
        """execute"""

        # Get dates
        date_end = datetime.now()
        date_start = date_end.replace(day=1)
        date_start_str = date_start.strftime("%Y-%m-%d")
        date_end_str = date_end.strftime("%Y-%m-%d")

        print("Date Start :", date_start_str)
        print("Date End   :", date_end_str)

        # Get session
        session = Session()
        session.headers.update({"User-Agent": UA})

        # Get on login page to fill cookies
        login_page_url = f"{base_url}/Login"
        session.get(login_page_url)
        # Send post request to auth endpoint
        auth_url = f"{base_url}/Start/Index"
        response = session.post(
            auth_url,
            data={
                "login": login,
                "password": password,
                "stay_signed": 0,
            },
        )

        # Check if logged in correctly
        if b"wykladowcath" not in response.content:
            send_telegram_notification(
                "Nie udało się zalogować do Niebieski.net",
                TelegramChats.OTHER,
            )
            exit(0)

        # Go to stat page to fill cookies
        session.get(f"{base_url}/StatTransfer")

        # Get stats
        response = session.post(
            f"{base_url}/StatTransfer/Index",
            data={
                "NAV[page]": 0,
                "NAV[start_date]": date_start_str,
                "NAV[end_date]": date_end_str,
                "stat-transfer-search-submit": None,
            },
        )

        # Get Values
        html_content = str(response.content, "utf8")
        tree = html.fromstring(html_content)

        # Wygenerowano
        def normalize_str(string: str):
            ret = string.strip().replace("\n", "")
            for _ in range(10):
                ret = ret.replace(2 * " ", " ")
            return ret.strip()

        # Stworz wiadomosc telegram
        idxs = [1, 2, 3, 4, 5, 6]
        msg = f"# Zużycie Niebieski.net [{alias}]:\n\n"
        for idx in idxs:
            base = "/html/body/div[1]/div[2]/div/div[2]/div[4]/div[1]/ul"
            kp = f"{base}/li[{idx}]/span/text()"
            vp = f"{base}/li[{idx}]/span/strong/text()"
            k: str = normalize_str(tree.xpath(kp)[0])
            v: str = normalize_str(tree.xpath(vp)[0])
            print(repr(k), repr(v))
            msg += f"{k}: {v}\n"

        # Wyslij wiadomosc
        send_telegram_notification(
            msg,
            TelegramChats.OTHER,
        )

    def handle(self, *args, **options):

        profiles = [
            (
                "ZAPYTANIE 111",
                "https://webas5105.niebieski.net",
                settings.NIEBIESKI_ZAPYTANIE_1_LOGIN,
                settings.NIEBIESKI_ZAPYTANIE_1_PASSWORD,
            ),
            (
                "ZAPYTANIE 222",
                "https://webas5222.niebieski.net",
                settings.NIEBIESKI_ZAPYTANIE_2_LOGIN,
                settings.NIEBIESKI_ZAPYTANIE_2_PASSWORD,
            ),
        ]

        for alias, base_url, login, password in profiles:
            try:
                self.execute_command(alias, base_url, login, password)
                print("OK")
            except Exception as e:  # pylint: disable=broad-exception-caught
                print("KO")
                send_telegram_notification(
                    f"Wystąpił błąd podczas próby pobrania zużycia (Niebieski): {e}",
                    TelegramChats.OTHER,
                )
