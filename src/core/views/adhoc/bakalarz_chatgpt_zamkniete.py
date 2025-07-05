"""bakalarz_chatgpt_zamkniete"""

# flake8: noqa=E501

from django.template.response import TemplateResponse

from core.forms import ClosedWebinarContactForm


def bakalarz_chatgpt_zamkniete(request):
    """bakalarz_chatgpt_zamkniete"""

    form = ClosedWebinarContactForm()
    return TemplateResponse(
        request, "geeks/pages/adhoc/bakalarz_chatgpt_zamkniete.html", {"form": form}
    )
