from django.template.response import TemplateResponse


def krajowy_fundusz_szkoleniowy_page(request):
    """Krajowy fundusz szkoleniowy page"""
    template_name = "geeks/pages/KrajowyFunduszSzkoleniowyPage.html"
    return TemplateResponse(request, template_name, {})
