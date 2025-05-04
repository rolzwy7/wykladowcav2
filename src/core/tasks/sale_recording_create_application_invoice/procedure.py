# flake8: noqa

from core.libs.fakturownia import create_proforma_for_sale_recording_application
from core.models import SaleRecordingApplication


def sale_recording_create_application_invoice(
    application_id: int,
):
    """Create invoice for application"""
    application = SaleRecordingApplication.manager.get(id=application_id)
    return create_proforma_for_sale_recording_application(application)
