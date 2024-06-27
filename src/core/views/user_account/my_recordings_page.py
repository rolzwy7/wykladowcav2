"""my Recordings Page"""

# flake8: noqa


from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from core.models import WebinarRecordingToken


@login_required(login_url="/logowanie/")
def my_recordings_page(request):
    """Page with user's recorings"""

    template_name = "geeks/pages/user_account/MyRecordingsPage.html"

    if request.user.is_authenticated and request.user.contributor:
        return TemplateResponse(
            request,
            template_name,
            {
                "recording_tokens": WebinarRecordingToken.manager.get_tokens_for_unique_recordings()
            },
        )
    else:
        return TemplateResponse(
            request,
            template_name,
            {
                "recording_tokens": WebinarRecordingToken.manager.get_tokens_by_participant_email(
                    request.user.email
                )
            },
        )
