from django.template.response import TemplateResponse


def editor_email_page(request, pk):
    """Email editor page"""
    return TemplateResponse(request, "geeks/pages/EditorEmailPage.html", {"pk": pk})
