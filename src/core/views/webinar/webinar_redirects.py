"""webinar redirects"""

# flake8: noqa=E501

from django.db.models import F
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now

from core.libs.mongo.db import MongoDBClient
from core.models import MailingCampaign, Webinar, WebinarMetadata


def webinar_redirect_to_program(request: HttpRequest, pk: int):
    """Redirect to webinar program by webinar ID"""
    webinar: Webinar = get_object_or_404(Webinar, pk=pk)

    WebinarMetadata.objects.filter(webinar=webinar).update(
        click_count_mailing=F("click_count_mailing") + 1
    )

    return redirect(
        reverse("core:webinar_program_page", kwargs={"slug": webinar.slug})
        + f"?utm_medium=email&utm_source=mailing&utm_campaign={webinar.slug}"
    )


def webinar_redirect_to_program_tracking(
    request: HttpRequest, pk: int, tracking_code: str
):
    """Redirect to webinar program by webinar ID"""
    webinar: Webinar = get_object_or_404(Webinar, pk=pk)

    if len(tracking_code) <= 32:
        request.session["tracking_code"] = tracking_code

    return redirect(
        reverse("core:webinar_redirect_to_program_safe", kwargs={"pk": webinar.id})
    )


def webinar_redirect_to_program_tracking_and_campaign_id(
    request: HttpRequest, pk: int, tracking_code: str, campaign_id: int
):
    """Redirect to webinar program by webinar ID"""
    # webinar: Webinar = get_object_or_404(Webinar, pk=pk)
    # get_object_or_404(MailingCampaign, pk=campaign_id)

    if request.user.is_staff:  # type: ignore
        return redirect(
            reverse("core:webinar_redirect_to_program_safe", kwargs={"pk": pk})
        )

    request.session["campaign_id"] = str(campaign_id)

    if len(tracking_code) <= 32:
        request.session["tracking_code"] = tracking_code

    MailingCampaign.manager.filter(id=campaign_id).update(
        total_clicks=F("total_clicks") + 1
    )

    try:
        _, database = MongoDBClient.get_connection()
        database["wykladowcav2_mailing_clicks"].insert_one(
            {
                "tracking_code": tracking_code,
                "campaign_id": campaign_id,
                "request_url": request.build_absolute_uri(),
                "datetime": now(),
                "ip_address": request.META.get("REMOTE_ADDR"),
                "user_agent": request.META.get("HTTP_USER_AGENT"),
            }
        )
    except Exception as e:
        pass

    return redirect(reverse("core:webinar_redirect_to_program_safe", kwargs={"pk": pk}))


def webinar_redirect_to_program_onesignal(request: HttpRequest, pk: int):
    """Redirect to webinar program by webinar ID"""
    webinar: Webinar = get_object_or_404(Webinar, pk=pk)
    metadata = WebinarMetadata.objects.get(webinar=webinar)
    metadata.click_count_onesignal += 1
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
    return redirect(reverse("core:application_type_page", kwargs={"pk": webinar.pk}))
