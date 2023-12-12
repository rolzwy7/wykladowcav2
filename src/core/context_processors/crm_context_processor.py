# flake8: noqa:501
# pylint: disable=line-too-long
from django.http import HttpRequest

from core.models import ContactMessage, CrmTodo, Webinar
from core.models.mailing import MailingCampaign


def crm(request: HttpRequest):
    """CRM context processor"""
    if not request.path.startswith("/crm/"):
        return {}

    return {
        "CRM_LEFBAR_TODO_LEFT_COUNT": CrmTodo.manager.filter(is_done=False).count(),
        "CRM_LEFBAR_ARCHIVE_COUNT": Webinar.manager.get_done_or_canceled_webinars().count(),
        "CRM_LEFBAR_WEBINAR_COUNT": Webinar.manager.get_init_or_confirmed_webinars().count(),
        "CRM_LEFBAR_ACTIVE_MAILING_CAMPAIGNS": MailingCampaign.manager.active_campaigns().count(),
        "CRM_CONTACT_MESSAGE_NEWSET_COUNT": ContactMessage.manager.newest_count(),
    }
