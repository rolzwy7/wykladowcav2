"""Command: RBL check"""

# flake8: noqa=E501

from django.core.management.base import BaseCommand, CommandError

from core.libs.rbl import run_monitoring_for_item

# Załóżmy, że model SmtpSender znajduje się w aplikacji 'senders'
# Zmień 'senders.models' na właściwą ścieżkę do Twojego modelu.
from core.models import SmtpSender


class Command(BaseCommand):
    help = "Sprawdza wszystkie domeny i adresy IP z modelu SmtpSender na listach RBL."

    def handle(self, *args, **options):
        if SmtpSender is None:
            raise CommandError(
                "Nie można zaimportować modelu SmtpSender. "
                "Upewnij się, że ścieżka importu jest poprawna."
            )

        self.stdout.write(
            self.style.SUCCESS("Rozpoczynam sprawdzanie RBL dla SmtpSender...")
        )

        # Używamy seta, aby uniknąć wielokrotnego sprawdzania tych samych domen/IP
        items_to_check = set()

        senders = SmtpSender.objects.all()
        if not senders.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Nie znaleziono żadnych obiektów SmtpSender do sprawdzenia."
                )
            )
            return

        for sender in senders:
            if not sender.monitor_rbl:
                self.stdout.write(
                    self.style.WARNING(f"{sender} - monitorowanie RBL wyłączone")
                )
                continue
            if sender.domain:
                items_to_check.add(sender.domain)
            if sender.ip_address:
                items_to_check.add(sender.ip_address)

        if not items_to_check:
            self.stdout.write(
                self.style.WARNING(
                    "Brak domen lub adresów IP do sprawdzenia w obiektach SmtpSender."
                )
            )
            return

        self.stdout.write(
            f"Znaleziono {len(items_to_check)} unikalnych elementów do sprawdzenia."
        )

        for item in items_to_check:
            try:
                run_monitoring_for_item(item)
                self.stdout.write(
                    self.style.SUCCESS(f"Pomyślnie zakończono sprawdzanie dla: {item}")
                )
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f"Wystąpił błąd podczas sprawdzania '{item}': {e}")
                )

        self.stdout.write(self.style.SUCCESS("Zakończono zadanie sprawdzania RBL."))
