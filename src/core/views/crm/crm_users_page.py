"""CRM Users Page"""

# flake8: noqa=E501

from django.template.response import TemplateResponse

from core.models import User


def crm_users_page(request):
    """crm_users_page"""
    template_name = "core/pages/crm/CrmUsers.html"

    search_query = request.GET.get("q")
    if search_query:
        users = User.objects.filter(username__icontains=search_query)
    else:
        users = User.objects.all()

    return TemplateResponse(
        request, template_name, {"users": users, "search_query": search_query or ""}
    )
