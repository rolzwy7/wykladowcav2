from django.urls import reverse

from core.models import Lecturer, LecturerOpinion, Webinar


class LecturerService:
    """Lecturer service"""

    def __init__(self, lecturer: Lecturer) -> None:
        self.lecturer = lecturer

    def get_lecturer_webinars(self):
        """Get lecturer webinars"""
        return Webinar.manager.homepage_webinars().filter(
            lecturer=self.lecturer
        )

    def get_lecturer_opinions(self):
        """Get opinions about lecturer"""
        return LecturerOpinion.objects.filter(visible_on_page=True).order_by(
            "-created_at"
        )

    def get_lecturer_tabs(self, tab_index: int):
        """Returns structure of lecturer tabs

        Args:
            tab_index (int): tab to be active

        Returns:
            list[tuple]: structure of lecturer tabs
        """
        tabs = [
            (
                "O wykładowcy",
                "core:lecturer_experience_page",
                "ki-book-open",
            ),
            (
                "Szkolenia",
                "core:lecturer_webinars_page",
                "ki-like-shapes",
            ),
            (
                "Opinie",
                "core:lecturer_opinions_page",
                "ki-price-tag",
            ),
        ]
        _tab_index = (
            tab_index if all([tab_index >= 0, tab_index < len(tabs)]) else 0
        )
        return [
            (
                title,  # tab title
                reverse(url_name, kwargs={"slug": self.lecturer.slug}),  # url
                idx == _tab_index,  # is active
                icon,  # icon
            )
            for idx, (title, url_name, icon) in enumerate(tabs)
        ]
