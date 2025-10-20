# flake8: noqa=E501

from django.db.models import Q
from django.template.response import TemplateResponse

from core.models import SaleRecordingApplication, SaleRecordingParticipant
from core.models.enums import SaleRecordingApplicationStatus


def crm_sold_recordings(request):
    """crm_sold_recordings"""

    if request.GET.get("show_all"):
        qs = SaleRecordingApplication.manager.all()
    else:
        qs = SaleRecordingApplication.manager.filter(
            Q(status=SaleRecordingApplicationStatus.WAITING_FOR_PAYMENT)
            | Q(status=SaleRecordingApplicationStatus.PAYED)
        )

    sale_recording_applications = [
        (
            _application,
            SaleRecordingParticipant.manager.filter(application=_application),
        )
        for _application in qs
    ]

    return TemplateResponse(
        request,
        "core/pages/crm/CrmRecordingsSoldList.html",
        {
            "sale_recording_applications": sale_recording_applications,
            "param_show_all": request.GET.get("show_all"),
        },
    )
