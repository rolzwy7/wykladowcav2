from django.conf import settings
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
    def get_main_categories_with_counts():
        """Get all main categories with counts"""

        cache_key = "CACHED_MAIN_CATEGORIES_WITH_COUNTS"

        if not settings.DEBUG and cache.get(cache_key):
            return cache.get(cache_key)

        categories = []
        for category in WebinarCategory.manager.get_main_categories():
            categories.append(
                (
                    category,
                    Webinar.manager.get_active_webinars_for_category_slugs(
                        [category.slug]
                    ).count(),
                )
            )

        cache.set(cache_key, categories, 600)

        return categories
