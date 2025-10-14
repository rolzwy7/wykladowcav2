"""
Mailing sending procedure
"""

# flake8: noqa:E501
# pylint: disable=global-variable-not-assigned
# pylint: disable=broad-exception-caught
# pylint: disable=unused-variable
# pylint: disable=invalid-name

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.template.defaultfilters import date as _date
from django.utils.timezone import get_default_timezone, now, timedelta

from core.consts import TelegramChats
from core.libs.justsend.send_sms import send_sms, sms_clean_phone_number
from core.libs.mailing.schedule import schedule_log, schedule_mailing
from core.models import MailingScheduled, WebinarParticipant
from core.models.enums import ApplicationStatus, MailingPoolStatus, WebinarStatus
from core.models.enums.mailing_enums import MailingScheduledStatus
from core.models.mailing import MailingPoolManager
from core.services import TelegramService


class Command(BaseCommand):
    """sms_reminders_dispatch"""

    help = "sms_reminders_dispatch"

    def add_arguments(self, parser): ...

    def handle(self, *args, **options):
        """handle"""

        tz = get_default_timezone()

        participants = WebinarParticipant.manager.filter(
            # Zgodzili sie na przypomnienie sms
            Q(sms_reminder_consent=True)
            # Nie wyslano jeszcze sms'a
            & Q(sms_reminder_send=False)
            # Nie bylo bledu podczas poprzedniej proby
            & Q(sms_error_msg="")
            # Termin jest potwierdzony
            & Q(application__webinar__status=WebinarStatus.CONFIRMED)
            # Tylko zgloszenia wyslane
            & Q(application__status=ApplicationStatus.SENT)
            # Jest minimalnie 1,5h przed szkoleniem, ale nie po starcie
            & (
                Q(application__webinar__date__gt=now())
                & Q(
                    application__webinar__date__lt=now()
                    + timedelta(hours=1, minutes=30)
                )
            )
        )

        telegram_service = TelegramService()

        for participant in participants:
            participant_id: int = participant.id
            phone_clean = sms_clean_phone_number(participant.phone)
            print(participant_id)
            print(participant)
            print(participant.phone, "-->", phone_clean)
            print("\n\n")

            if not phone_clean:
                WebinarParticipant.manager.filter(id=participant_id).update(
                    sms_error_msg="Nieprawidłowy numer"
                )
                print(">> INVALID PHONE NUMBER\n")
                continue

            webinar = participant.application.webinar
            hour = _date(webinar.date.astimezone(tz), "H:i")
            message = f"Przypominamy o szkoleniu dziś o {hour} - Zespół Wykladowca.pl"

            WebinarParticipant.manager.filter(id=participant_id).update(
                sms_error_msg="LOCK"
            )

            try:
                send_sms("Wykladowca", phone_clean, message)
            except Exception as e:
                WebinarParticipant.manager.filter(id=participant_id).update(
                    sms_error_msg=str(e)[:100]
                )
                print(">> ERROR\n")
            else:
                WebinarParticipant.manager.filter(id=participant_id).update(
                    sms_reminder_send=True, sms_reminder_send_dt=now(), sms_error_msg=""
                )
                print(">> SENT\n")
                telegram_service.try_send_chat_message(
                    f"SMS przypominający: {phone_clean}",
                    TelegramChats.OTHER,
                )
