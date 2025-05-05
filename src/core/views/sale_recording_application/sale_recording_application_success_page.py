# flake8: noqa=E501

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import SaleRecordingApplication, Webinar


def sale_recording_application_success_page(request, uuid):
    """Application success page"""

    template_name = "geeks/pages/sale_recording_application/ApplicationSuccessPage.html"
    application = get_object_or_404(SaleRecordingApplication, uuid=uuid)
    webinar: Webinar = application.sale_recording.recording.webinar

    return TemplateResponse(
        request,
        template_name,
        {
            "application": application,
            "webinar": webinar,
        },
    )
