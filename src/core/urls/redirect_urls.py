from django.urls import path

from core.views.redirects import redirect_manual_endpoint

urlpatterns = [
    path(
        "<slug:slug_a>/",
        redirect_manual_endpoint,
        name="redirect_manual",
    ),
    path(
        "<slug:slug_a>/<slug:slug_b>/",
        redirect_manual_endpoint,
        name="redirect_manual",
    ),
    path(
        "<slug:slug_a>/<slug:slug_b>/<slug:slug_c>/",
        redirect_manual_endpoint,
        name="redirect_manual",
    ),
]
