"""telegram message"""

# flake8: noqa=E501

from django.core.management.base import BaseCommand, CommandError

from core.consts import TelegramChats
from core.services import TelegramService


class Command(BaseCommand):
    """
    Komenda Django do wysyłania wiadomości na Telegram.

    Przykład użycia:
    python manage.py send_telegram_message "To jest Twoja testowa wiadomość"
    """

    help = "Wysyła podaną wiadomość tekstową na kanał Telegram."

    def add_arguments(self, parser):
        """Dodaje argumenty wiersza poleceń."""
        parser.add_argument(
            "message", type=str, help="Wiadomość, która ma zostać wysłana."
        )

    def handle(self, *args, **options):
        """Główna logika komendy."""
        message = options["message"]

        if not message:
            raise CommandError("Wiadomość nie może być pusta.")

        self.stdout.write(f"Próba wysłania wiadomości: '{message}'...")

        try:
            telegram_service = TelegramService()
            telegram_service.try_send_chat_message(
                message,
                TelegramChats.OTHER,  # Domyślny czat, zgodnie z przykładem
            )
            self.stdout.write(
                self.style.SUCCESS("✅ Wiadomość została pomyślnie wysłana!")
            )
        except Exception as e:
            raise CommandError(f"❌ Wystąpił błąd podczas wysyłania wiadomości: {e}")
