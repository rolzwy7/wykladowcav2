"""crm_mailing_dobijanie"""

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.consts.requests_consts import POST
from core.libs.mailing.export import export_emails_mongo_index_tags
from core.models import Webinar


def crm_mailing_dobijanie(request, pk):
    """crm_mailing_dobijanie"""
    template_name = "core/pages/crm/mailing/MailingDobijanie.html"

    webinar = get_object_or_404(Webinar, pk=pk)

    index_tags = export_emails_mongo_index_tags()

    if request.method == POST:
        ...
    #     form = MailingSendTestEmailForm(request.POST)
    #     if form.is_valid():
    #         email = form.cleaned_data["email"]

    #         send_campaign_test_email(email, mailing_campaign)

    #         return redirect(
    #             reverse(
    #                 "core:crm_mailing_campaign_detail",
    #                 kwargs={"pk": mailing_campaign.pk},
    #             )
    #         )
    else:
        ...
        # form = MailingSendTestEmailForm()

    return TemplateResponse(
        request,
        template_name,
        {"webinar": webinar, "tags": index_tags},
    )
