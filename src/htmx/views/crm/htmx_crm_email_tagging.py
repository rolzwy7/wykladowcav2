from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse

from core.consts import INIT_TAGS, POST, WEBMAILS
from core.models.tagging import TaggedEmailManager
from core.services import BlacklistService


def htmx_crm_email_tagging_toggle(request: HttpRequest, email: str, tag: str):
    """Tag email"""

    template_path = "htmx/tagging/htmx_crm_email_tagging_toggle.html"

    manager = TaggedEmailManager()
    document = manager.get_or_create_tagged_email(email)
    if not document:
        return HttpResponse("document doesn't exist")

    tag_present = tag in document["tags"]

    if request.method == POST:
        if tag_present:
            tag_present = False
            manager.delete_tags_from_email(email, [tag])
        else:
            tag_present = True
            manager.add_tags_to_email(email, [tag])

    manager.close()

    return TemplateResponse(
        request,
        template_path,
        {
            "email": email,
            "tag": tag,
            "tag_present": tag_present,
        },
    )


def htmx_crm_email_tagging_init(request: HttpRequest, email: str):
    """Tag email init panel"""
    template_path = "htmx/tagging/htmx_crm_email_tagging_init.html"

    manager = TaggedEmailManager()
    document = manager.get_or_create_tagged_email(email)
    if not document:
        return HttpResponse("document doesn't exist")
    manager.close()

    _, domain = email.split("@")

    is_webmail = WEBMAILS.get(domain, False)

    blacklist_service = BlacklistService()
    is_dangerous = blacklist_service.is_email_dangerous_to_send(email)

    tags = sorted(list(set([*document["tags"], *INIT_TAGS])))
    tags = [
        (idx * 150, tag) for idx, tag in enumerate(tags) if tag in INIT_TAGS
    ]

    return TemplateResponse(
        request,
        template_path,
        {
            "email": email,
            "tags": tags,
            "is_dangerous": is_dangerous,
            "is_webmail": is_webmail,
        },
    )
