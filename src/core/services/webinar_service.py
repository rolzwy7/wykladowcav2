from django.urls import reverse
from django.utils.timezone import now

from core.models import Webinar


class WebinarService:
    """Webinar service"""

    def __init__(self, webinar: Webinar) -> None:
        self.webinar = webinar

    def get_discount_progress_bar_data(self) -> tuple[str, str]:
        """Get % width and color of discount progess bar"""
        discount_until = self.webinar.discount_until
        if discount_until and discount_until > now():
            remaining_seconds = (discount_until - now()).total_seconds()
            base_seconds = 3 * 24 * 60 * 60
            percent = min(remaining_seconds / base_seconds, 1.0)
            if percent <= 0.8:
                color = "danger"
            else:
                color = "success"

            return f"{percent:.2%}", color

        return "0%", "primary"

    def get_webinar_tabs(self, tab_index: int):
        """Returns structure of webinar tabs

        Args:
            tab_index (int): tab to be active

        Returns:
            list[tuple]: _description_
        """
        tabs = [
            (
                "Program szkolenia",
                "core:webinar_program_page",
                "ki-book-open",
            ),
            (
                "Opinie",
                "core:webinar_opinions_page",
                "ki-like-shapes",
            ),
            (
                "Cena i Faktura",
                "core:webinar_price_and_invoice_page",
                "ki-price-tag",
            ),
            (
                "O wykładowcy",
                "core:webinar_lecturer_biography_page",
                "ki-teacher",
            ),
        ]
        _tab_index = (
            tab_index if all([tab_index >= 0, tab_index < len(tabs)]) else 0
        )
        return [
            (
                title,  # tab title
                reverse(url_name, kwargs={"slug": self.webinar.slug}),  # url
                idx == _tab_index,  # is active
                icon,  # icon
            )
            for idx, (title, url_name, icon) in enumerate(tabs)
        ]

    def get_context(self):
        """Get common context"""
        (
            discount_progress_percent,
            discount_progress_color,
        ) = self.get_discount_progress_bar_data()
        return {
            "discount_progress_percent": discount_progress_percent,
            "discount_progress_color": discount_progress_color,
        }
