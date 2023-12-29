"""
Webinr category mailing editor page
"""

# flake8: noqa=E501

from django.template.response import TemplateResponse


def webinar_category_mailing_editor_page(request, slug: str):
    """Mailing editor page for webinar category"""

    return TemplateResponse(
        request,
        "mailing_templates/MailingWebinarCategoryList/WebinarCategoryMailingEditorPage.html",
        {"slug": slug},
    )
