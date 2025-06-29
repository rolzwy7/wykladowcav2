"""
Mailing sending procedure
"""

# flake8: noqa=E501

from django.core.management.base import BaseCommand

from core.models import MailingCampaign, MailingTitleTest


def testab_calculate_winner(ma: int, na: int, mb: int, nb: int):
    """
    Oblicz zwyciezce testu A/b

    Args:
        ma (int): ilosc konwersji A
        na (int): ilosc prób A
        mb (int): ilosc konwersji B
        nb (int): ilosc prób B
    """
    # 0,05	1,645
    # 0,01	2,3263
    # 0,001	3,09
    ...


class Command(BaseCommand):
    """Mailing subject TEST A/B"""

    help = "Mailing subject TEST A/B"

    def add_arguments(self, parser): ...

    def handle(self, *args, **options):
        """handle"""

        # Get active campaigns
        active_campaigns = MailingCampaign.manager.active_campaigns()

        contestants: list[tuple[int, str, int, int]] = []

        for active_campaign in active_campaigns:
            active_campaign_id: int = active_campaign.id  # type: ignore
            subjects = active_campaign.get_subjects()
            for subject in subjects:
                try:
                    title_test = MailingTitleTest.objects.get(
                        campaign_id=active_campaign_id, title=subject
                    )
                except MailingTitleTest.DoesNotExist:
                    ...  # TODO: subject nie istnieje, pomin
                else:
                    param_clicks = title_test.counter
                    param_sent = title_test.total_sent
                    contestants.append(
                        (active_campaign_id, subject, param_clicks, param_sent)
                    )

        ...
