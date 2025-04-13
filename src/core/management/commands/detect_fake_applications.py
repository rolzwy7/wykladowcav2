"""
Mailing sending procedure
"""

# flake8: noqa:E501
# pylint: disable=global-variable-not-assigned
# pylint: disable=broad-exception-caught
# pylint: disable=unused-variable
# pylint: disable=invalid-name

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.timezone import now

from core.consts import TelegramChats
from core.models import WebinarParticipant
from core.models.enums.application_enums import ApplicationStatus
from core.models.webinar_application_model import WebinarApplication
from core.services import TelegramService

TRIGGER_WORDS = [
    "chuj",
    "kurwa",
    "pierdol",
    "spam",
    " rodo ",
    " kara ",
    " karę ",
]


def fake_application_log_insert(application: WebinarApplication, log: str):
    """fake_application_log_insert"""

    timestamp = now().strftime("[%Y-%m-%d %H:%M:%S]")
    application_id: int = application.id  # type: ignore

    current_logs: str = WebinarApplication.manager.get(
        id=application_id
    ).fake_application_logs

    _log = f"{current_logs}{timestamp} {log}"
    print(f"{timestamp} {log}")
    WebinarApplication.manager.filter(id=application_id).update(
        fake_application_logs=f"{_log}\n"
    )


class Command(BaseCommand):
    """Detect fake applications"""

    help = "Detect fake applications"

    def add_arguments(self, parser): ...

    def handle(self, *args, **options):
        """handle"""

        applications = WebinarApplication.manager.filter(
            Q(status=ApplicationStatus.SENT) & Q(fake_application_logs="")
        ).order_by("-created_at")

        for application in applications:
            application_id: int = application.id
            participants = WebinarParticipant.manager.filter(application=application)

            print("Application:", application)
            values_map = {
                "application.additional_information": application.additional_information
            }

            for idx, participant in enumerate(participants):
                values_map[f"participant-{idx}-first_name"] = participant.first_name
                values_map[f"participant-{idx}-last_name"] = participant.last_name
                values_map[f"participant-{idx}-email"] = participant.email
                values_map[f"participant-{idx}-phone"] = participant.phone

            if application.buyer:
                values_map = {
                    **values_map,
                    "application.buyer": application.buyer,
                    "application.buyer.name": application.buyer.name,
                    "application.buyer.address": application.buyer.address,
                    "application.buyer.postal_code": application.buyer.postal_code,
                    "application.buyer.city": application.buyer.city,
                    "application.buyer.email": application.buyer.email,
                    "application.buyer.phone_number": application.buyer.phone_number,
                }

            if application.recipient:
                values_map = {
                    **values_map,
                    "application.recipient": application.recipient,
                    "application.recipient.name": application.recipient.name,
                    "application.recipient.address": application.recipient.address,
                    "application.recipient.postal_code": application.recipient.postal_code,
                    "application.recipient.city": application.recipient.city,
                    "application.recipient.email": application.recipient.email,
                    "application.recipient.phone_number": application.recipient.phone_number,
                }

            if application.private_person:
                values_map = {
                    **values_map,
                    "application.private_person": application.private_person,
                    "application.private_person.first_name": application.private_person.first_name,
                    "application.private_person.last_name": application.private_person.last_name,
                    "application.private_person.address": application.private_person.address,
                    "application.private_person.postal_code": application.private_person.postal_code,
                    "application.private_person.city": application.private_person.city,
                    "application.private_person.email": application.private_person.email,
                    "application.private_person.phone": application.private_person.phone,
                }

            if application.invoice:
                values_map = {
                    **values_map,
                    "application.invoice": application.invoice,
                    "application.invoice.invoice_email": application.invoice.invoice_email,
                    "application.invoice.invoice_additional_info": application.invoice.invoice_additional_info,
                }

            if application.submitter:
                values_map = {
                    **values_map,
                    "application.submitter": application.submitter,
                    "application.submitter.first_name": application.submitter.first_name,
                    "application.submitter.last_name": application.submitter.last_name,
                    "application.submitter.email": application.submitter.email,
                    "application.submitter.phone": application.submitter.phone,
                }

            is_fake = False
            temp_logs: list[str] = []
            for key_name, key_value in values_map.items():
                for trigger_word in TRIGGER_WORDS:
                    if trigger_word.lower() in str(key_value).lower():
                        is_fake = True
                        temp_log = (
                            f"Fraza '{trigger_word}' w '{key_name}': '{key_value}'"
                        )
                        temp_logs.append(temp_log)
                        fake_application_log_insert(application, temp_log)

            if is_fake:
                print("[!] Fałszywe zgłoszenie\n")
                WebinarApplication.manager.filter(id=application_id).update(
                    fake_application=is_fake
                )
                joined_logs = "\n".join(temp_logs)
                telegram_msg = f"[?FAŁSZYWE_ZGŁOSZENIE?] Zgłoszenie numer: {application_id}\n\n{joined_logs}"

                print("telegram_msg:", telegram_msg)
                if not settings.DEBUG:
                    telegram_service = TelegramService()
                    telegram_service.try_send_chat_message(
                        telegram_msg,
                        TelegramChats.OTHER,
                    )
            else:
                print("[+] Czyste zgłoszenie\n")
                fake_application_log_insert(application, "Czyste zgłoszenie")
