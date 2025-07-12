"""bakalarz_chatgpt_zamkniete"""

# flake8: noqa=E501

from django.template.response import TemplateResponse

from core.forms import ClosedWebinarContactForm


def bakalarz_chatgpt_zamkniete(request):
    """bakalarz_chatgpt_zamkniete"""

    template_name = "geeks/pages/adhoc/bakalarz_chatgpt_zamkniete.html"

    form = ClosedWebinarContactForm()
    return TemplateResponse(request, template_name, {"form": form})


def bakalarz_chatgpt_zamkniete_no_work(request):
    """bakalarz_chatgpt_zamkniete"""

    template_name = "geeks/pages/adhoc/bakalarz_chatgpt_zamkniete_no_work.html"

    form = ClosedWebinarContactForm()
    return TemplateResponse(request, template_name, {"form": form})
