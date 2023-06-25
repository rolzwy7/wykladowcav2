from django.db.models import Q

from core.models import (
    WebinarApplication,
    WebinarApplicationSubmitter,
    WebinarParticipant,
)


def save_submitter_as_participant(
    application: WebinarApplication, submitter: WebinarApplicationSubmitter
):
    # Is user selected `is_participant`
    # and there is not participant with submitter's email already
    # in participants then save submitter as participant
    is_submiter_in_participants = WebinarParticipant.objects.filter(
        Q(application=application) & Q(email=submitter.email)
    ).exists()
    if all(
        [
            submitter.is_participant is True,
            not is_submiter_in_participants,
        ]
    ):
        WebinarParticipant(
            application=application,
            first_name=submitter.first_name,
            last_name=submitter.last_name,
            email=submitter.email,
            phone=submitter.phone,
        ).save()
