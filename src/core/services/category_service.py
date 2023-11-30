from django.core.cache import cache
from django.db.models import Q

from core.models import Lecturer, LecturerOpinion, Webinar, WebinarCategory


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

    @staticmethod
    def get_all_categories_with_counts():
        """Get all categories with counts"""

        if cache.get("CATEGORIES_WITH_COUNTS"):
            return cache.get("CATEGORIES_WITH_COUNTS")

        categories = []
        for category in WebinarCategory.manager.get_main_categories():
            if category.slug == "wszystkie-szkolenia":
                count = Webinar.manager.get_active_webinars().count()
                categories.append((category, count))
            else:
                count = Webinar.manager.get_active_webinars_for_category_slugs(
                    [category.slug]
                ).count()
                categories.append((category, count))

        cache.set("CATEGORIES_WITH_COUNTS", categories, 600)
        return categories
