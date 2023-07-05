from django.urls import path

from core.views.certificate import certificate_pdf_page

urlpatterns = [
    path(
        "pdf/<uuid:uuid>/",
        certificate_pdf_page,
        name="certificate_pdf_page",
    )
]
