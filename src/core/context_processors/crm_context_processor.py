# flake8: noqa:501
# pylint: disable=line-too-long
from django.http import HttpRequest

from core.models import CrmTodo, Webinar
from core.models.mailing import MailingCampaign


def crm(request: HttpRequest):
    """CRM context processor"""
    if not request.path.startswith("/crm/"):
        return {}

    return {
        "CRM_LEFBAR_TODO_LEFT_COUNT": CrmTodo.objects.filter(
            is_done=False
        ).count(),
        "CRM_LEFBAR_ARCHIVE_COUNT": Webinar.manager.done_or_canceled().count(),
        "CRM_LEFBAR_WEBINAR_COUNT": Webinar.manager.init_or_confirmed().count(),
        "CRM_LEFBAR_ACTIVE_MAILING_CAMPAIGNS": MailingCampaign.manager.active_campaigns().count(),
    }
