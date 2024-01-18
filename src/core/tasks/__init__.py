# flake8: noqa
from .create_application_invoice import task_create_application_invoice
from .create_clickmeeting_room import (
    params_create_clickmeeting_room,
    task_create_clickmeeting_room,
)
from .create_crm_todo import task_create_crm_todo
from .create_eventlog import params_create_eventlog, task_create_eventlog
from .create_participant_certificate import task_create_participant_certificate
from .download_and_process_clickmeeting_recording import (
    task_download_and_process_clickmeeting_recording,
)
from .save_application_invoice_metadata import task_save_application_invoice_metadata
from .send_clickmeeting_invitation_lecturer import (
    task_send_clickmeeting_invitation_lecturer,
)
from .send_clickmeeting_invitation_participant import (
    task_send_clickmeeting_invitation_participant,
)
from .send_free_participant_conference_email import (
    params_send_free_participant_conference_email,
    task_send_free_participant_conference_email,
)
from .send_invoice_email import task_send_invoice_email
from .send_participant_certificate_email import (
    params_send_participant_certificate_email,
    task_send_participant_certificate_email,
)
from .send_participant_confirmation_email import (
    params_send_participant_confirmation_email,
    task_send_participant_confirmation_email,
)
from .send_participant_opinion_email import (
    params_send_participant_opinion_email,
    task_send_participant_opinion_email,
)
from .send_participant_preparation_email import (
    params_send_participant_preparation_email,
    task_send_participant_preparation_email,
)
from .send_participant_recording_email import (
    params_send_participant_recording_email,
    task_send_participant_recording_email,
)
from .send_submitter_cancellation_email import (
    params_send_submitter_cancellation_email,
    task_send_submitter_cancellation_email,
)
from .send_submitter_confirmation_email import (
    params_send_submitter_confirmation_email,
    task_send_submitter_confirmation_email,
)
from .send_submitter_moving_email import (
    params_send_submitter_moving_email,
    task_send_submitter_moving_email,
)
from .send_telegram_notification import task_send_telegram_notification
