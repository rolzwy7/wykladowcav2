"""RBL Lib"""

# flake8: noqa=E501

import ipaddress
from typing import Dict, Union

import dns.resolver

from core.consts import TelegramChats

# Załóżmy, że te modele znajdują się w tej samej aplikacji Django
from core.models import ListRBL, MonitorRBL
from core.services import TelegramService


def _reverse_ip(ip: str) -> str:
    """
    Odwraca oktety adresu IP.
    np. "1.2.3.4" staje się "4.3.2.1".
    """
    return ".".join(reversed(ip.split(".")))


def check_item_on_rbl(item: str, rbl_server: str) -> Dict[str, Union[bool, str]]:
    """
    Sprawdza, czy dany adres IP lub domena znajduje się na konkretnej liście RBL.
    Do działania wymaga biblioteki 'dnspython'.
    Instalacja: pip install dnspython

    Args:
        item: Adres IP lub domena do sprawdzenia.
        rbl_server: Adres serwera RBL (np. 'zen.spamhaus.org').

    Returns:
        Słownik zawierający:
        - 'is_blacklisted': bool
        - 'response': Tekst odpowiedzi DNS lub komunikat o błędzie.
    """
    query_address = ""
    try:
        # Sprawdzenie, czy 'item' jest poprawnym adresem IP
        ip_obj = ipaddress.ip_address(item)
        if ip_obj.version == 4:
            query_address = f"{_reverse_ip(item)}.{rbl_server}"
        else:
            # Sprawdzanie IPv6 jest rzadsze i bardziej skomplikowane.
            return {
                "is_blacklisted": False,
                "response": "Sprawdzanie adresów IPv6 nie jest obsługiwane w tej wersji.",
            }
    except ValueError:
        # Jeśli to nie jest adres IP, traktujemy go jako domenę
        query_address = f"{item}.{rbl_server}"

    try:
        # Wykonanie zapytania DNS typu 'A'
        answers = dns.resolver.resolve(query_address, "A")
        # Każda odpowiedź (zazwyczaj z puli 127.0.0.x) oznacza wpis na liście.
        response_text = (
            f"Na liście! Odpowiedź: {', '.join([str(r.address) for r in answers])}"
        )
        return {"is_blacklisted": True, "response": response_text}
    except dns.resolver.NXDOMAIN:
        # NXDOMAIN to oczekiwana odpowiedź dla czystego elementu.
        return {"is_blacklisted": False, "response": "Nie ma na liście (NXDOMAIN)."}
    except dns.resolver.NoAnswer:
        # Brak rekordu 'A', ale domena istnieje. Może oznaczać wpis bez dodatkowych informacji.
        return {"is_blacklisted": True, "response": "Na liście! (NoAnswer)"}
    except dns.exception.Timeout:
        return {
            "is_blacklisted": False,
            "response": "Przekroczono czas oczekiwania na odpowiedź DNS.",
        }
    except Exception as e:
        return {
            "is_blacklisted": False,
            "response": f"Wystąpił nieoczekiwany błąd: {str(e)}",
        }


def run_monitoring_for_item(item: str):
    """
    Uruchamia sprawdzanie danego elementu (IP lub domeny) na wszystkich
    istotnych listach RBL z bazy danych i zapisuje wyniki.
    Ta funkcja powinna być wywoływana np. z zadania Celery lub komendy zarządzania Django.
    """

    telegram_service = TelegramService()

    is_ip = False
    try:
        ipaddress.ip_address(item)
        is_ip = True
    except ValueError:
        pass  # Jeśli nie jest to IP, jest to domena

    # Ustal, które listy RBL należy odpytać
    if is_ip:
        lists_to_query = ListRBL.manager.filter(list_type__in=["ip", "ip_domain"])
    else:  # jest to domena
        lists_to_query = ListRBL.manager.filter(list_type__in=["domain", "ip_domain"])

    print(f"Rozpoczynam sprawdzanie '{item}'...")
    for rbl in lists_to_query:
        print(f"-> Sprawdzam na liście: {rbl.address}...")
        result = check_item_on_rbl(item, rbl.address)

        last_result = MonitorRBL.manager.get_latest(item, rbl)

        if last_result:
            telegram_msg = ""
            if last_result.is_blacklisted is True and result["is_blacklisted"] is False:
                telegram_msg = f"✅ `{item}` został ściągnięty z listy RBL `{rbl}`"
            if last_result.is_blacklisted is False and result["is_blacklisted"] is True:
                telegram_msg = f"🛑 `{item}` został dodany do listy RBL `{rbl}`"
            if telegram_msg:
                telegram_service.try_send_chat_message(
                    telegram_msg,
                    TelegramChats.OTHER,
                )

        # Zapisz wynik do bazy danych
        MonitorRBL.manager.create(
            monitored_item=item,
            rbl_list=rbl,
            response=result["response"],
            is_blacklisted=result["is_blacklisted"],
        )
        print(f"   Wynik: {result['response']}")
    print(f"Zakończono sprawdzanie '{item}'.")
