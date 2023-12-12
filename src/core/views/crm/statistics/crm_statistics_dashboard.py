# flake8: noqa=E501
# pylint: disable=line-too-long

from django.template.response import TemplateResponse

from core.models import LoyaltyProgram, User


def crm_statistics_dashboard(request):
    """CRM statistics dashboard"""
    template_name = "core/pages/crm/statistics/CrmStatisticsDashboard.html"

    non_staff_users_count = User.objects.filter(is_staff=False).count()

    return TemplateResponse(
        request,
        template_name,
        {
            "loyalty_program_users_count": LoyaltyProgram.manager.all().count(),
            "non_staff_users_count": non_staff_users_count,
        },
    )
