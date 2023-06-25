from core.models import (
    WebinarApplication,
    WebinarApplicationInvoice,
    WebinarApplicationPrivatePerson,
    WebinarApplicationSubmitter,
    WebinarParticipant,
)


def populate_private_person_data(
    application: WebinarApplication,
    private_person: WebinarApplicationPrivatePerson,
):
    """Populate application fields based on private person data

    Args:
        application (WebinarApplication): application
        private_person (WebinarApplicationPrivatePerson): private person data
    """

    # Save participant
    # Delete all participants and save new one
    WebinarParticipant.objects.filter(application=application).delete()
    WebinarParticipant(
        application=application,
        first_name=private_person.first_name,
        last_name=private_person.last_name,
        email=private_person.email,
        phone=private_person.phone,
    ).save()

    # Save invoice
    if application.invoice:
        invoice = application.invoice
        invoice.invoice_email = private_person.email
    else:
        invoice = WebinarApplicationInvoice(invoice_email=private_person.email)
        application.invoice = invoice  # type: ignore

    invoice.save()

    # Save submitter
    if application.submitter:
        submitter = application.submitter
        submitter.first_name = private_person.first_name
        submitter.last_name = private_person.last_name
        submitter.email = private_person.email
        submitter.phone = private_person.phone
    else:
        submitter = WebinarApplicationSubmitter(
            first_name=private_person.first_name,
            last_name=private_person.last_name,
            email=private_person.email,
            phone=private_person.phone,
        )
        application.submitter = submitter  # type: ignore

    submitter.save()
    application.save()
