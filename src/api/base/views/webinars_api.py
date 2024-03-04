"""Webinars API endpoints"""

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from api.base.serializers import WebinarModelSerializer
from core.models import Webinar


class WebinarViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Webinar.manager.all()
    serializer_class = WebinarModelSerializer
