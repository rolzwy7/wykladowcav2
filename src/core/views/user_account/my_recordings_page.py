from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from core.models import WebinarRecordingToken


@login_required(login_url="/logowanie/")
def my_recordings_page(request):
    """Page with user's recorings"""

    recording_tokens = WebinarRecordingToken.manager.filter(
        participant__email=request.user.email
    )

    return TemplateResponse(
        request,
        "geeks/pages/user_account/MyRecordingsPage.html",
        {"recording_tokens": recording_tokens},
    )
