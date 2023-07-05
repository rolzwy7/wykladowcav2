from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("cms/", admin.site.urls),
    path("api/", include("api.urls", namespace="api")),
    path("", include("core.urls", namespace="core")),
]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )  # type: ignore
