"""API routers"""

from rest_framework import routers

from api.base.views.webinars_api import WebinarViewSet

router = routers.DefaultRouter()
router.register("webinar", WebinarViewSet)
