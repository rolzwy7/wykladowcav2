"""Thanks page"""

# flake8: noqa=E501
# pylint: disable=line-too-long

from django.http import HttpResponseNotFound
from django.template.response import TemplateResponse


def thanks_page(request, choice_slug: str):
    """thanks_page"""

    if choice_slug not in ["przypomnij-o-terminie"]:
        return HttpResponseNotFound()

    h1_title = "Dziękujemy"
    p_text = ""

    if choice_slug == "przypomnij-o-terminie":
        h1_title = "Dziękujemy za zainteresowanie!"
        p_text = "Gdy tylko pojawią się nowe terminy związane z wybranym tematem, wyślemy Ci przypomnienie."

    template_path = "geeks/pages/ThanksPage.html"
    return TemplateResponse(
        request,
        template_path,
        {"choice_slug": choice_slug, "h1_title": h1_title, "p_text": p_text},
    )
