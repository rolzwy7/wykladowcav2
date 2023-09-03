from core.models import Lecturer, Webinar


class HomepageService:
    """Homepage service"""

    def __init__(self):
        pass

    def get_our_clients(self):
        """Get `our clients` data (logo urls and company names)"""
        logos_base = "media/our-clients-logos"
        return [
            (f"{logos_base}/allegro.svg", "Allegro"),
            (f"{logos_base}/cinema_city.svg", "Cinema City"),
            # (f"{logos_base}/comarch.svg", "Comarch"),
            (f"{logos_base}/kghm.svg", "KGHM"),
            (f"{logos_base}/pge.svg", "PGE"),
            (f"{logos_base}/pocztapolska.svg", "Poczta Polska"),
        ]

    def get_context(self):
        """Get context for homepage"""
        return {
            "webinars": Webinar.manager.get_active_webinars(),
            "visible_lecturers": Lecturer.manager.get_lecturers_visible_on_page(),
            "our_clients": self.get_our_clients(),
        }
