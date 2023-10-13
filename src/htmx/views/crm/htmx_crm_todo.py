from django.http import HttpRequest, HttpResponse

from core.models import CrmTodo


def htmx_crm_toggle_todo(request: HttpRequest, pk: int):
    """Toggle CRM To-Do `is_done` field"""
    todo = CrmTodo.objects.get(pk=pk)
    todo.is_done = not todo.is_done
    todo.save()
    return HttpResponse("")
