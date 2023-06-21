from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.consts import POST
from core.forms import LoginForm


def login_page(request):
    template_name = "core/pages/LoginPage.html"
    auth_failed = False

    next_param = request.GET.get("next")

    if request.method == POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_param or reverse("core:dashboard_page"))
            else:
                auth_failed = True
    else:
        if request.user.is_authenticated:
            return redirect(reverse("core:dashboard_page"))
        form = LoginForm()

    return TemplateResponse(
        request,
        template_name,
        {"form": form, "auth_failed": auth_failed, "next_param": next_param},
    )
