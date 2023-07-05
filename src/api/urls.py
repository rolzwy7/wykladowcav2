from django.urls import path

from api.base.views.regon import regon_autocomplete
from api.base.views.todos import crm_todo_toggle_done

app_name = "api"

urlpatterns = [
    path("regon-autocomplete/", regon_autocomplete, name="regon-autocomplete"),
    path(
        "crm-toggle-todo/<int:pk>/",
        crm_todo_toggle_done,
        name="crm_todo_toggle_done",
    ),
]
