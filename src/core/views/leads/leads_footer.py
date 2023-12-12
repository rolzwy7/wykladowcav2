from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

from core.consts.requests_consts import POST
from core.models import WebinarCategory
from core.models.enums import LeadSource
from core.services import LeadService


def lead_footer_post_endpoint(request: HttpRequest):
    """lead_footer_post_endpoint"""

    if request.method == POST:
        email = request.POST["email"]

        # Get or create lead object
        lead = LeadService.get_or_create_lead(
            email, LeadSource.NEWSLETTER_FOOTER, request=request
        )

        # Try to save category if set
        category_id = request.POST.get("category", "0")
        if category_id != "0":
            category = WebinarCategory.manager.get(id=int(category_id))
            lead.preferences.add(category)

    return redirect(reverse("core:leads_thanks_page"))
