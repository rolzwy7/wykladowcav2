from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from core.models import Webinar, WebinarMetadata


def webinar_redirect_to_program(request: HttpRequest, pk: int):
    """Redirect to webinar program by webinar ID"""
    webinar: Webinar = get_object_or_404(Webinar, pk=pk)
    metadata = WebinarMetadata.objects.get(webinar=webinar)
    metadata.click_count_mailing += 1
    metadata.save()

    return redirect(
        reverse("core:webinar_program_page", kwargs={"slug": webinar.slug})
        + f"?utm_medium=email&utm_source=mailing&utm_campaign={webinar.slug}"
    )


def webinar_redirect_to_program_onesignal(request: HttpRequest, pk: int):
    """Redirect to webinar program by webinar ID"""
    webinar: Webinar = get_object_or_404(Webinar, pk=pk)
    metadata = WebinarMetadata.objects.get(webinar=webinar)
    metadata.click_count_mailing += 1
    metadata.save()

    return redirect(
        reverse("core:webinar_program_page", kwargs={"slug": webinar.slug})
        + f"?utm_medium=push&utm_source=onesignal&utm_campaign={webinar.slug}"
    )


def webinar_redirect_to_program_facebook(request: HttpRequest, pk: int):
    """Redirect to webinar program by webinar ID"""
    webinar: Webinar = get_object_or_404(Webinar, pk=pk)
    metadata = WebinarMetadata.objects.get(webinar=webinar)
    metadata.click_count_facebook += 1
    metadata.save()
    return redirect(
        reverse("core:webinar_program_page", kwargs={"slug": webinar.slug})
        + f"?utm_medium=social&utm_source=facebook&utm_campaign={webinar.slug}"
    )


def webinar_redirect_to_application(request: HttpRequest, pk: int):
    """Redirect to application by webinar ID"""
    webinar: Webinar = get_object_or_404(Webinar, pk=pk)
    return redirect(
        reverse("core:application_type_page", kwargs={"pk": webinar.pk})
    )
