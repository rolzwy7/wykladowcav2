from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse

from core.models.tagging import TaggedEmailManager
from core.services import TaggingService


def crm_tagging_iframe_mirror(request: HttpRequest):
    """CRM tagging iframe mirror"""
    url = request.GET.get("url", "")
    service = TaggingService()
    _, _, html = service.download_page(url)
    emails = service.find_all_emails(str(html, "utf8"))

    content = html if html else b"Error"

    def get_highlighted_email(email: str):
        return f"""<span
        style='background-color:red;color:white;font-weight:bold;padding:5px;'>
        {email}</span>"""

    for email in emails:
        content = content.replace(
            email.encode("utf8"), get_highlighted_email(email).encode("utf8")
        )

    headers = {"X-Frame-Options": "SAMEORIGIN"}
    return HttpResponse(content, headers=headers)


# TODO: cache this?
def crm_tagging_tool(request: HttpRequest):
    """Tagging tool"""
    template_path = "core/pages/crm/tagging/CrmTaggingTool.html"
    url = request.GET.get("url", "")
    service = TaggingService()
    response_ok, status_code, html = service.download_page(url)

    if response_ok:
        emails = service.find_all_emails(str(html, "utf8"))
    else:
        emails = []

    if status_code >= 200 and status_code < 300:
        color = "success"
    else:
        color = "danger"

    return TemplateResponse(
        request,
        template_path,
        {
            "url": url,
            "status_code": status_code,
            "emails": emails,
            "color": color,
        },
    )


# TODO: crm_tagging_dashboard_page
def crm_tagging_dashboard_page(request: HttpRequest):
    """Tagging dashboard page"""
    template_path = "core/pages/crm/tagging/CrmTaggingDashboardPage.html"

    manager = TaggedEmailManager()
    all_emails_count = manager.get_all_emails_count()
    untagged_emails_count = manager.get_untagged_emails_count()
    manager.close()

    return TemplateResponse(
        request,
        template_path,
        {
            "all_emails_count": all_emails_count,
            "untagged_emails_count": untagged_emails_count,
        },
    )


# TODO: crm_export_tagged_emails_page
def crm_export_tagged_emails_page(request: HttpRequest):
    """Export tagged emails page"""
    ...
