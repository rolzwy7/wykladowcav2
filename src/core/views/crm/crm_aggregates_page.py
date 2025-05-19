"""crm_aggregates_page"""

from django.template.response import TemplateResponse

from core.models import WebinarAggregate


def crm_aggregates_page(request):
    """crm_aggregates_page"""
    template_name = "core/pages/crm/CrmAggregates.html"

    aggregates = WebinarAggregate.manager.all()

    return TemplateResponse(request, template_name, {"aggregates": aggregates})
