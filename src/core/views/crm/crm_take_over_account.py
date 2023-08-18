from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from core.models import User
from core.permissions import deny_if_not_staff


@login_required(login_url="/logowanie/")
def crm_take_over_account(request: HttpRequest):
    """CRM take over account"""
    deny_if_not_staff(request.user)
    template_name = "core/pages/crm/CrmTakeOverAccount.html"
    user_id = request.GET.get("user_id", "")

    if user_id:
        user = get_object_or_404(User, pk=int(user_id))
        login(request, user)
        return redirect(reverse("core:homepage"))

    return TemplateResponse(request, template_name, {})
