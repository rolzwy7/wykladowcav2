from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse


def logout_page(request):
    """Logout controller"""
    logout(request)
    return redirect(reverse("core:homepage"))
