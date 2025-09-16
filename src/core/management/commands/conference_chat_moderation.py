"""
Management command do ciągłego przetwarzania i moderowania
wiadomości na czacie konferencji.
"""

# flake8: noqa=E501
# pylint: disable=line-too-long

import time

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from core.consts.aggressor_phrases import AGGRESSOR_PHRASES_ICONTAINS
from core.models import ConferenceChatMessage
from core.models.conference.chat_message_status_enum import ChatMessageStatusEnum


class Command(BaseCommand):
    """
    Komenda Django do moderacji wiadomości na czacie w nieskończonej pętli.
    """

    help = "Uruchamia proces do ciągłej moderacji wiadomości na czacie."

    def handle(self, *args, **options):
        """Główna metoda komendy."""
        self.stdout.write(self.style.SUCCESS("Uruchamianie procesu moderacji czatu..."))
        self.stdout.write("Naciśnij CTRL+C, aby zakończyć.")

        try:
            while True:
                any_init_messages = self.process_init_messages()
                self.process_auto_admin_messages()

                # Krótka pauza, aby nie obciążać nadmiernie bazy danych
                self.stdout.write("Czekam na nowe wiadomości (pauza 5 sekund)...")
                time.sleep(10)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\nZatrzymywanie procesu moderacji."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Wystąpił krytyczny błąd: {e}"))

    def process_init_messages(self):
        """
        Przetwarza wiadomości ze statusem INIT.
        Sprawdza, czy zawierają zabronione słowa.

        True - były wiadomości do przetowrzenia, False - nie było
        """
        self.stdout.write(
            "Krok 1: Sprawdzanie wiadomości INIT pod kątem zabronionych słów."
        )
        messages_to_process = ConferenceChatMessage.objects.filter(
            status=ChatMessageStatusEnum.INIT
        )

        if not messages_to_process:
            self.stdout.write("Brak wiadomości INIT do przetworzenia.")
            return False

        forbidden_phrases = AGGRESSOR_PHRASES_ICONTAINS
        self.stdout.write(f"Znaleziono {messages_to_process.count()} wiadomości.")

        for msg in messages_to_process:
            message_lower = msg.message.lower()
            is_aggressor = any(
                phrase.lower() in message_lower for phrase in forbidden_phrases
            )

            with transaction.atomic():
                if is_aggressor:
                    msg.status = ChatMessageStatusEnum.AGGRESSOR
                    self.stdout.write(
                        self.style.WARNING(
                            f"Wiadomość {msg.id} oznaczona jako AGGRESSOR."
                        )
                    )
                else:
                    msg.status = ChatMessageStatusEnum.AUTO_ADMIN
                    self.stdout.write(
                        f"Wiadomość {msg.id} przekazana do analizy (AUTO_ADMIN)."
                    )
                msg.save()

        return True

    def process_auto_admin_messages(self):
        """
        Przetwarza wiadomości ze statusem AUTO_ADMIN.
        Wysyła je do analizy przez Perspective API.
        """
        self.stdout.write(
            "Krok 2: Analiza wiadomości AUTO_ADMIN przez Perspective API."
        )
        messages_to_analyze = ConferenceChatMessage.objects.filter(
            status=ChatMessageStatusEnum.AUTO_ADMIN
        )

        if not messages_to_analyze:
            self.stdout.write("Brak wiadomości AUTO_ADMIN do analizy.")
            return

        if not settings.PERSPECTIVE_API_KEY:
            self.stderr.write(
                self.style.ERROR(
                    "Brak klucza PERSPECTIVE_API_KEY w settings.py. Przerywam analizę."
                )
            )
            # Dodaj wszystkie do recznej moderacji jak nie ma klucza
            for msg in messages_to_analyze:
                with transaction.atomic():
                    msg.status = ChatMessageStatusEnum.MANUAL_ADMIN
                    self.stdout.write(
                        self.style.NOTICE(
                            f"Wyjątek -> Wiadomość {msg.id} do ręcznej moderacji"
                        )
                    )
                    msg.save()
            return

        url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={settings.PERSPECTIVE_API_KEY}"

        self.stdout.write(
            f"Znaleziono {messages_to_analyze.count()} wiadomości do analizy."
        )

        for msg in messages_to_analyze:
            payload = {
                "comment": {"text": msg.message},
                "languages": ["pl"],
                "requestedAttributes": {"TOXICITY": {}},
            }
            was_exception = False

            try:
                response = requests.post(url, json=payload, timeout=5)
                response.raise_for_status()
                data = response.json()

                toxicity_score = data["attributeScores"]["TOXICITY"]["summaryScore"][
                    "value"
                ]
                score_percent = int(toxicity_score * 100)

                with transaction.atomic():
                    msg.perspective_score = score_percent
                    if toxicity_score < 0.05:
                        msg.status = ChatMessageStatusEnum.ACCEPTED
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Wiadomość {msg.id} zaakceptowana (Score: {score_percent}%)."
                            )
                        )
                    else:
                        msg.status = ChatMessageStatusEnum.MANUAL_ADMIN
                        self.stdout.write(
                            self.style.NOTICE(
                                f"Wiadomość {msg.id} do ręcznej moderacji (Score: {score_percent}%)."
                            )
                        )
                    msg.save()

            except requests.RequestException as e:
                was_exception = True
                self.stderr.write(
                    self.style.ERROR(f"Błąd API dla wiadomości {msg.id}: {e}")
                )
            except (KeyError, TypeError) as e:
                was_exception = True
                self.stderr.write(
                    self.style.ERROR(
                        f"Nieprawidłowa odpowiedź API dla wiadomości {msg.id}: {e}"
                    )
                )

            if was_exception:
                self.stderr.write(self.style.ERROR(f"Wyjątek {msg.id}"))
                with transaction.atomic():
                    msg.status = ChatMessageStatusEnum.MANUAL_ADMIN
                    self.stdout.write(
                        self.style.NOTICE(
                            f"Wyjątek -> Wiadomość {msg.id} do ręcznej moderacji"
                        )
                    )
                    msg.save()
