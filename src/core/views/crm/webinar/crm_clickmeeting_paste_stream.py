"""CRM webinar analysis"""

# flake8: noqa=E501
# pylint: disable=no-member

from django.shortcuts import get_object_or_404, redirect

from core.models import ConferenceEdition, Webinar


def crm_clickmeeting_paste_stream(request, pk: int):
    """crm_clickmeeting_paste_stream"""

    webinar = get_object_or_404(Webinar, pk=pk)
    edition: ConferenceEdition = ConferenceEdition.manager.get(webinar=webinar)
    clickmeeting_id = edition.clickmeeting_id

    edition.clickmeeting_pasted = True
    edition.save()

    return redirect(
        f"https://account-panel.clickmeeting.com/{clickmeeting_id}/edit#settings"
    )
