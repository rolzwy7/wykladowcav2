from django.urls import path

from core.views import webinar_category_page

urlpatterns = [
    path("<slug:slug>/", webinar_category_page, name="webinar_category_page")
]
