from core.models import Webinar


class WebinarMovingService:
    """Webinar moving service"""

    def __init__(self, webinar: Webinar) -> None:
        self.webinar = webinar

    def move_webinar(self):
        ...
