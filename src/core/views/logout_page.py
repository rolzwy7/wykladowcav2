from django.contrib.auth import logout
from django.template.response import TemplateResponse


def logout_page(request):
    template_name = "core_app/pages/LogoutPage.html"
    logout(request)
    return TemplateResponse(request, template_name, {})
