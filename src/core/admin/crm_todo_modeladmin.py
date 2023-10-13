from django.contrib.admin import ModelAdmin, register

from core.models import CrmTodo


@register(CrmTodo)
class CrmTodoModelAdmin(ModelAdmin):
    ...
