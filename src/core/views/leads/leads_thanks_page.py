from django.http import HttpRequest
from django.template.response import TemplateResponse


def leads_thanks_page(request: HttpRequest):
    """leads_thanks_page"""

    template_name = "geeks/pages/leads/LeadsThankYouPage.html"
    return TemplateResponse(request, template_name, {})
