"""dev_command"""

# flake8: noqa=E501
from django.core.management.base import BaseCommand
from django.urls import reverse

from core.consts import TelegramChats
from core.models import Webinar, WebinarAggregate
from core.services import TelegramService


class Command(BaseCommand):
    """dev_command"""

    help = "dev_command"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        telegram_service = TelegramService()

        for aggregate in WebinarAggregate.manager.get_active_aggregates():

            dates: list[str] = []

            for _webinar in aggregate.webinars.all():
                webinar: Webinar = _webinar

                if not webinar.is_active:
                    continue

                dates.append(webinar.human_date)

            if len(dates) != len(set(dates)):
                url = "https://wykladowca.pl" + reverse(
                    "core:webinar_aggregate_page", kwargs={"slug": aggregate.slug}
                )
                msg = f"🛑 Zdublowany termin w agregacie {url}"

                telegram_service.try_send_chat_message(
                    msg,
                    TelegramChats.OTHER,
                )
