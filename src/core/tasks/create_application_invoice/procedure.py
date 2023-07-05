from core.libs.fakturownia import create_invoice_for_application
from core.models import WebinarApplication


def create_application_invoice(
    application_id: int,
):
    """Create invoice for application"""
    application = WebinarApplication.manager.get(id=application_id)
    return create_invoice_for_application(application)
