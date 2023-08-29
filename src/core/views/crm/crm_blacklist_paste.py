from django.template.response import TemplateResponse

from core.consts import POST
from core.forms.crm import CrmBlacklistPasteForm
from core.services import BlacklistService


def crm_blacklist_paste(request):
    """CRM paste blacklist"""
    template_name = "core/pages/crm/CrmBlacklistPaste.html"

    result_blacklisted = []
    result_skipped = []

    if request.method == POST:
        form = CrmBlacklistPasteForm(request.POST)
        if form.is_valid():
            blacklist_lines = form.cleaned_data["blacklist_lines"]
            for line in blacklist_lines.split("\n"):
                temp = line.strip("\r\n")
                blacklisted, ret_line = BlacklistService.try_to_blacklist_line(
                    temp
                )
                if blacklisted:
                    result_blacklisted.append(ret_line)
                else:
                    result_skipped.append(ret_line)
    else:
        form = CrmBlacklistPasteForm()

    return TemplateResponse(
        request,
        template_name,
        {
            "result_blacklisted": result_blacklisted,
            "result_skipped": result_skipped,
        },
    )
