from core.models import Lecturer, Webinar, WebinarCategory


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

    def get_homepage_lecturers(self):
        """Get lecturers for homepage"""
        return Lecturer.manager.get_lecturers_visible_on_homepage().order_by(
            "order_value"
        )[:4]

    def get_context(self):
        """Get context for homepage"""
        return {
            "categories": WebinarCategory.manager.get_main_categories(),
            "webinars": Webinar.manager.get_active_webinars(),
            "homepage_lecturers": self.get_homepage_lecturers(),
            "our_clients": self.get_our_clients(),
        }
