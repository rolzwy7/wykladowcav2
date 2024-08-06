"""Homepage service"""

# flake8: noqa

from django.db.models import Q

from core.models import CrmCompany, Lecturer, Webinar


class HomepageService:
    """Homepage service"""

    def __init__(self):
        pass

    def get_our_clients(self):
        """Get `our clients` data (logo urls and company names)"""
        return (
            CrmCompany.objects.filter(
                Q(avatar__isnull=False) & Q(logo_visible_on_page=True)
            )
            .exclude(avatar="")
            .order_by("page_ordering")
        )

    def get_homepage_lecturers(self):
        """Get lecturers for homepage"""
        return Lecturer.manager.get_lecturers_visible_on_homepage().order_by(
            "order_value"
        )[:8]

    def get_context(self):
        """Get context for homepage"""
        return {
            "webinars": Webinar.manager.get_active_webinars(),
            "homepage_lecturers": self.get_homepage_lecturers(),
            "our_clients": self.get_our_clients(),
        }
