from rest_framework.decorators import (
    api_view,
    renderer_classes,
    throttle_classes,
)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.base.throttling import RegonAutocompleteThrottle
from core.services import RegonService


@api_view(["POST"])
@renderer_classes([JSONRenderer])  # policy decorator
@throttle_classes([RegonAutocompleteThrottle])
def regon_autocomplete(request):
    """Return company data from REGON"""

    service = RegonService()
    nip: str = request.data["nip"]

    return Response(service.get_application_autocomplete(nip).dict())
