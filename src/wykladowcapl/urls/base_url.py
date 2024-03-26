"""Base URLs"""

# flake8: noqa=E501

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import meta_redirect_page, one_signal_worker_script
from core.views.changelog_page import changelog_page
from core.views.robots_page import robots_page

from .sitemap_urls import sitemap_xml_path

urlpatterns = [
    path("cms/", admin.site.urls),
    path("api/", include("api.urls", namespace="api")),
    path("api-auth/", include("rest_framework.urls")),
    path("htmx/", include("htmx.htmx_urls", namespace="htmx")),
    path("tinymce/", include("tinymce.urls")),
    path("r/", meta_redirect_page, name="meta_redirect_page"),
    # SEO
    sitemap_xml_path,
    path("robots.txt", robots_page, name="robots_page"),
    path("changelog.txt", changelog_page, name="changelog_page"),
    # OneSignal
    path(
        "OneSignalSDKWorker.js",
        one_signal_worker_script,
        name="one_signal_worker_script",
    ),
    # Django Debug Toolbar
    path("__debug__/", include("debug_toolbar.urls"), name="debug_toolbar"),
    path("", include("core.urls", namespace="core")),
]


handler404 = "core.views.custom404_page"
handler500 = "core.views.custom500_page"

if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )  # type: ignore
