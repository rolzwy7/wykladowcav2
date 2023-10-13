from django.db.models import Q

from core.models import Lecturer, LecturerOpinion, WebinarCategory


class CategoryService:
    """Category service"""

    def __init__(self, category: WebinarCategory) -> None:
        self.category = category

    def get_lecturers_for_category(self):
        """Get lecturers for given category"""
        return Lecturer.manager.get_lecturers_visible_on_page().filter(
            categories__in=[self.category]
        )

    def get_opinions_for_category(self):
        """Get lecturers opinions for given category"""
        lecturers = self.get_lecturers_for_category()
        lecturers_ids: list[int] = [_.id for _ in lecturers]  # type: ignore
        return LecturerOpinion.manager.filter(
            Q(visible_on_page=True) & Q(lecturer__id__in=lecturers_ids)
        )
