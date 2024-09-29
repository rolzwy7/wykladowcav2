"""API routers"""

from rest_framework import routers

from api.base.views.survey_api import SurveyViewSet
from api.base.views.webinars_api import WebinarViewSet

router = routers.DefaultRouter()
router.register("webinar", WebinarViewSet)
router.register("survey", SurveyViewSet)
