# flake8: noqa=E501

from django.template.response import TemplateResponse

from core.models import WebinarAggregate


def crm_images_list(request):
    """crm_images_list"""

    param_show_all = request.GET.get("show_all") == "1"
    if param_show_all:
        aggregates = WebinarAggregate.manager.all()
    else:
        aggregates = WebinarAggregate.manager.get_active_aggregates()

    return TemplateResponse(
        request,
        "core/pages/crm/CrmImagesList.html",
        {
            "aggregates": aggregates,
            "param_show_all": param_show_all,
        },
    )
