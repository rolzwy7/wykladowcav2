import random

from core.models import Lecturer, Webinar


class HomepageService:
    """Homepage service"""

    def __init__(self):
        pass

    def get_our_clients(self):
        """Get `our clients` data (logo urls and company names)"""
        logos_base = "media/our-clients-logos"
        return random.sample(
            [
                (f"{logos_base}/allegro.svg", "Allegro"),
                (f"{logos_base}/cinema_city.svg", "Cinema City"),
                (f"{logos_base}/comarch.svg", "Comarch"),
                (f"{logos_base}/kghm.svg", "KGHM"),
                (f"{logos_base}/pge.svg", "PGE"),
                (f"{logos_base}/pocztapolska.svg", "Poczta Polska"),
                # (f"{logos_base}/deutsche_bahn.svg", "Deutsche Bahn"),
                # (f"{logos_base}/hydro_vacuum.svg", "Hydro Vacuum"),
                (f"{logos_base}/jsw_sa.svg", "JSW SA"),
                (f"{logos_base}/orbis_sa.svg", "Orbis SA"),
            ],
            k=5,
        )

    def get_homepage_lecturers(self):
        """Get lecturers for homepage"""
        return Lecturer.manager.get_lecturers_visible_on_homepage().order_by(
            "order_value"
        )[:4]

    def get_context(self):
        """Get context for homepage"""
        return {
            "webinars": Webinar.manager.get_active_webinars(),
            "homepage_lecturers": self.get_homepage_lecturers(),
            "our_clients": self.get_our_clients(),
        }
