"""
Widoki Django dla panelu moderacji.
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from core.models import ConferenceChat


def chat_moderation_view(request: HttpRequest, id: str):
    """
    Renderuje stronę panelu moderacji dla konkretnego czatu.
    """
    template_name = "core/pages/crm/ChatModeration.html"
    chat = get_object_or_404(ConferenceChat, id=id)

    if not chat:
        return HttpResponse("Brak chatu")

    # Przekazujemy ID czatu do kontekstu, aby JavaScript mógł go użyć
    context = {
        "chat": chat,
    }

    return render(request, template_name, context)
