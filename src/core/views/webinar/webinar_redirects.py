from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from core.models import Webinar


def webinar_redirect_to_program(request: HttpRequest, pk: int):
    """Redirect to webinar program by webinar ID"""
    webinar: Webinar = get_object_or_404(Webinar, pk=pk)
    return redirect(
        reverse("core:webinar_program_page", kwargs={"slug": webinar.slug})
    )


def webinar_redirect_to_application(request: HttpRequest, pk: int):
    """Redirect to application by webinar ID"""
    webinar: Webinar = get_object_or_404(Webinar, pk=pk)
    return redirect(
        reverse("core:application_type_page", kwargs={"pk": webinar.pk})
    )
