from django.core.paginator import Page, Paginator
from django.db.models import Count, QuerySet

from core.models import LecturerOpinion
from core.models.enums import LecturerOpinionRating

RATING_MAP = {
    LecturerOpinionRating.STARS_1: 1,
    LecturerOpinionRating.STARS_2: 2,
    LecturerOpinionRating.STARS_3: 3,
    LecturerOpinionRating.STARS_4: 4,
    LecturerOpinionRating.STARS_5: 5,
}


class OpinionsService:
    """Opinions service"""

    def __init__(self, opinions: QuerySet["LecturerOpinion"]) -> None:
        self.opinions = opinions

    def get_opinions_page(self, page_number: int, per_page: int = 20) -> Page:
        """Get paginator's page

        Args:
            page_number (int): Page number
            per_page (int, optional): Opinions per page. Defaults to 20.

        Returns:
            Page: Opinions page
        """
        paginator = Paginator(self.opinions, per_page)
        return paginator.get_page(page_number)

    def get_opinions_average(self) -> float:
        """Ge average from opinions"""
        # Get group-by-count queryset (by rating value)
        qs = self.opinions.values("rating").annotate(count=Count("rating"))
        # Get opinions count and values, multiply: count * value
        avg_nominator, avg_denominator = 0, 0
        for rating in qs:
            count = rating["count"]
            avg_denominator += count
            avg_nominator += count * RATING_MAP.get(rating["rating"])
        # If average denominator is 0 then just return 0
        if avg_denominator == 0:
            return 0.0
        # Otherwise calculate opinions average
        return round(avg_nominator / avg_denominator, 1)

    def get_opinions_breakdown(self):
        """Get opinions breakdown"""
        # Get group-by-count queryset (by rating value)
        qs = self.opinions.values("rating").annotate(count=Count("rating"))
        # Prepare rating map ordered from 5 stars to 1 star
        ratings_order_map = {
            LecturerOpinionRating.STARS_5: 0,
            LecturerOpinionRating.STARS_4: 0,
            LecturerOpinionRating.STARS_3: 0,
            LecturerOpinionRating.STARS_2: 0,
            LecturerOpinionRating.STARS_1: 0,
        }
        # Calculate percent base
        percent_base = 0
        for rating in qs:
            ratings_order_map[rating["rating"]] = rating["count"]
            percent_base += rating["count"]
        # If division by 0 then just return None
        if percent_base == 0:
            return None
        # Return opinions brakdown
        return [
            (
                rating_str,
                rating_count,
                int(round(100 * (rating_count / percent_base), 0)),
            )
            for rating_str, rating_count in ratings_order_map.items()
        ]
