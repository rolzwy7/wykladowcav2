"""dev_command"""

# flake8: noqa=E501

from django.core.management.base import BaseCommand

from core.consts import TelegramChats
from core.models import Webinar, WebinarApplication, WebinarCategory, WebinarParticipant
from core.services import TelegramService


class Command(BaseCommand):
    """Command"""

    help = "Category Order"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        parent_categories = [_ for _ in WebinarCategory.manager.get_main_categories()]
        new_map = {}
        total_value = 0

        for parent_category in parent_categories:

            print("### Parent category:", parent_category.id, parent_category)

            # GET TOTAL CATEGORY VALUE
            total_category_value = 0

            # Get number of active/visible aggragates for category
            webinars = Webinar.manager.get_active_webinars_for_category_slugs(
                [parent_category.slug]
            )

            for webinar in webinars:
                print("# Webinar:", webinar)
                applications = WebinarApplication.manager.sent_applications_for_webinar(
                    webinar
                )
                total_netto = 0
                for application in applications:
                    count_participants = WebinarParticipant.manager.get_valid_participants_for_application(
                        application
                    ).count()
                    total_netto += application.price_netto * count_participants
                    total_category_value += total_netto
                    total_value += total_netto
                    print("Application", application.id, "total netto", total_netto)  # type: ignore
                    print("total value", total_value)

            #
            new_map[parent_category.id] = total_category_value  # type: ignore

        modify_map = {}

        for kat_id, total_cat_value in new_map.items():
            if total_value == 0:
                continue

            modify_map[kat_id] = 100 - int(100 * total_cat_value / total_value)

        for kat_id, order_val in modify_map.items():
            print("Cat", kat_id, "new order value:", order_val)
            WebinarCategory.manager.filter(id=kat_id).update(order=order_val)

        telegram_service = TelegramService()
        telegram_service.try_send_chat_message(
            "Zreorganizowano kategorie na stronie głównej",
            TelegramChats.OTHER,
        )
