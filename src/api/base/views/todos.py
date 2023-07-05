from django.conf import settings
from django.http import HttpResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from core.models import CrmTodo

# TODO: This shouldn't be in controller
# movie this to separate service ???


@api_view(["POST", "OPTIONS"])
@renderer_classes([JSONRenderer])
def crm_todo_toggle_done(request, pk: int):
    todo = CrmTodo.objects.get(pk=pk)
    todo.is_done = not todo.is_done
    todo.save()
    return HttpResponse("")
