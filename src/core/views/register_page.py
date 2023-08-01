from django.template.response import TemplateResponse

from core.consts import POST
from core.forms import RegistrationForm


def register_page(request):
    """Register page"""
    template_name = "core/pages/RegisterPage.html"

    if request.method == POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            a = 1
            # TODO: Create account
            # TODO: Send verification e-mail
    else:
        form = RegistrationForm()

    return TemplateResponse(
        request,
        template_name,
        {"form": form},
    )
