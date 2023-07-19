from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import robots_page

from .sitemap_urls import sitemap_xml_path

urlpatterns = [
    path("cms/", admin.site.urls),
    path("api/", include("api.urls", namespace="api")),
    path("htmx/", include("htmx.urls", namespace="htmx")),
    path("tinymce/", include("tinymce.urls")),
    path("robots.txt", robots_page, name="robots_page"),
    sitemap_xml_path,
    path("", include("core.urls", namespace="core")),
]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )  # type: ignore
