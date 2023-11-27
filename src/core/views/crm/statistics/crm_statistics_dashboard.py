from django.template.response import TemplateResponse

from core.models import LoyaltyProgram


def crm_statistics_dashboard(request):
    """CRM statistics dashboard"""
    template_name = "core/pages/crm/statistics/CrmStatisticsDashboard.html"
    return TemplateResponse(
        request,
        template_name,
        {"loyalty_program_user_count": LoyaltyProgram.manager.all().count()},
    )
