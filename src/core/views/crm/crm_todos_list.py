from django.template.response import TemplateResponse

from core.models import CrmTodo


def crm_todos_list(request):
    """CRM To-Do List (not done)"""
    template_name = "core/pages/crm/todos/CrmToDoList.html"
    todos = CrmTodo.objects.filter(is_done=False)
    return TemplateResponse(
        request,
        template_name,
        {"todos": todos},
    )


def crm_todos_done_list(request):
    """CRM To-Do List (done)"""
    template_name = "core/pages/crm/todos/CrmToDoList.html"
    todos = CrmTodo.objects.filter(is_done=True)
    return TemplateResponse(
        request,
        template_name,
        {"todos": todos},
    )
