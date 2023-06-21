from django.urls import path

from core.views import lecturer_list_page

urlpatterns = [path("", lecturer_list_page, name="lecturer_list_page")]
