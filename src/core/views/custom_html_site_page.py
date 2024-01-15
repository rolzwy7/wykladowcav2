"""
Custom HTML site view
"""

# flake8: noqa=E501

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import CustomHtmlSite


def custom_html_site_page(request, slug: str):
    """Cusomt HTML site page"""
    site = get_object_or_404(CustomHtmlSite, slug=slug)
    template_name = "geeks/pages/custom_html_site/CustomHtmlSite.html"
    return TemplateResponse(request, template_name, {"slug": slug, "site": site})
