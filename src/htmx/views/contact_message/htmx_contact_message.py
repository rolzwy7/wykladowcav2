from django.http import HttpRequest
from django.template.response import TemplateResponse

from core.consts import POST
from core.forms import ContactMessageForm


def htmx_contact_message(request: HttpRequest):
    """Toggle CRM participant phoned"""
    template_path = "htmx/htmx_contact_message_form.html"

    related_to = request.GET.get("related_to", "")

    if request.method == POST:
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return TemplateResponse(
                request,
                "htmx/htmx_contact_message_form_success.html",
                {},
            )
    else:
        form = ContactMessageForm(initial={"related_to": related_to})

    return TemplateResponse(
        request,
        template_path,
        {"form": form},
    )
