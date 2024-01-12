# flake8: noqa=E501

from django.urls import reverse

from core.models import Lecturer, LecturerOpinion, Webinar


class LecturerService:
    """Lecturer service"""

    def __init__(self, lecturer: Lecturer) -> None:
        self.lecturer = lecturer
        self.lecturer_id: int = lecturer.id  # type: ignore

    def get_lecturer_webinars(self):
        """Get lecturer webinars"""
        return Webinar.manager.get_active_webinars_for_lecturer(self.lecturer_id)

    def get_lecturer_webinars_archived(self):
        """Get lecturer webinars archived"""
        return Webinar.manager.get_archived_webinars().filter(lecturer=self.lecturer_id)

    def get_lecturer_webinars_count(self):
        """Get count for lecturer webinars"""
        return self.get_lecturer_webinars().count()

    def get_lecturer_opinions(self):
        """Get opinions about lecturer"""
        return LecturerOpinion.manager.get_visible_opinions_for_lecturer(self.lecturer)

    def get_lecturer_opinions_count(self):
        """Get count for opinions about lecturer"""
        return self.get_lecturer_opinions().count()

    def get_lecturer_nearest_webinar(self):
        """Get nearest webinar for this lecturer"""
        return (
            Webinar.manager.get_active_webinars_for_lecturer(self.lecturer_id)
            .order_by("date")
            .first()
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
        _tab_index = tab_index if all([tab_index >= 0, tab_index < len(tabs)]) else 0
        return [
            (
                title,  # tab title
                reverse(url_name, kwargs={"slug": self.lecturer.slug}),  # url
                idx == _tab_index,  # is active
                icon,  # icon
            )
            for idx, (title, url_name, icon) in enumerate(tabs)
        ]
