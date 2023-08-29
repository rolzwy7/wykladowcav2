from django.template.response import TemplateResponse

from core.models import ContactMessage


def crm_contact_messages(request):
    """CRM contact messages"""
    template_name = "core/pages/crm/CrmContactMessagesList.html"

    contact_messages = ContactMessage.manager.crm_visible()

    return TemplateResponse(
        request,
        template_name,
        {"contact_messages": contact_messages},
    )
