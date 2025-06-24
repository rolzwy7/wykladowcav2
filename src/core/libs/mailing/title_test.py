"""mailing title test"""

from core.models import MailingTitleTest


def get_or_create_mailing_title_test(subject: str, campaign_id: str):
    """get_or_create_mailing_title_test"""

    try:
        title_test = MailingTitleTest.objects.get(
            campaign_id=campaign_id, title=subject
        )
    except MailingTitleTest.DoesNotExist:
        title_test = MailingTitleTest(campaign_id=campaign_id, title=subject)
        title_test.save()

    return title_test
