from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse

from core.consts import INIT_TAGS, POST
from core.forms import TaggingAddEmailsForm
from core.models.mailing import SmtpSender
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


# TODO: cache this? delete this?
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
            "senders": SmtpSender.objects.all(),
            "untagged_emails_count": untagged_emails_count,
            "INIT_TAGS": INIT_TAGS,
        },
    )


def crm_tagging_paste_text_page(request: HttpRequest):
    """Tagging dashboard page"""
    template_path = "core/pages/crm/tagging/CrmTaggingPasteTextPage.html"
    service = TaggingService()

    if request.method == POST:
        text = request.POST["text"].lower()
        emails = service.find_all_emails(text)
    else:
        emails = []

    emails = sorted(list(set(emails)))
    emails = [(idx * 2000, email) for idx, email in enumerate(emails)]

    return TemplateResponse(
        request,
        template_path,
        {"emails": emails},
    )


def crm_tagging_import_emails_page(request: HttpRequest, tag: str):
    """Tagging dashboard page"""
    template_path = "core/pages/crm/tagging/CrmTaggingImportEmailsPage.html"

    not_in_init_tags = tag not in INIT_TAGS
    remove_tags: bool = True if request.GET.get("remove_tags") else False

    service = TaggingService()

    if request.method == POST:
        form = TaggingAddEmailsForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
            service.load_emails_from_file_into_tagging(
                file, tag, remove_tags=remove_tags
            )

    return TemplateResponse(
        request,
        template_path,
        {
            "tag": tag,
            "remove_tags": remove_tags,
            "not_in_init_tags": not_in_init_tags,
        },
    )


def crm_tagging_tag_by_domains_page(request: HttpRequest, tag: str):
    """Tagging dashboard page"""
    template_path = "core/pages/crm/tagging/CrmTaggingTagByDomainsPage.html"

    not_in_init_tags = tag not in INIT_TAGS
    remove_tags: bool = True if request.GET.get("remove_tags") else False

    service = TaggingService()

    if request.method == POST:
        form = TaggingAddEmailsForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
            service.load_file_tag_emails_by_domain(
                file, tag, remove_tags=remove_tags
            )

    return TemplateResponse(
        request,
        template_path,
        {
            "tag": tag,
            "remove_tags": remove_tags,
            "not_in_init_tags": not_in_init_tags,
        },
    )


def crm_tag_single_email_page(
    request: HttpRequest,
):
    """Page for tagging single e-mail provided by user"""
    template_path = "core/pages/crm/tagging/CrmTagSingleEmailPage.html"

    email = request.GET.get("email", "")

    return TemplateResponse(request, template_path, {"email": email})


# TODO: crm_export_tagged_emails_page
def crm_export_tagged_emails_page(request: HttpRequest):
    """Export tagged emails page"""
    ...
