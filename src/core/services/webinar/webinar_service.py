from django.db.models import Q
from django.urls import reverse

from core.models import Webinar


class WebinarService:
    """Webinar service"""

    def __init__(self, webinar: Webinar) -> None:
        self.webinar = webinar

    def get_related_webinars(self):
        """Get related webinars for this webinar"""
        webinar_id: int = self.webinar.id  # type: ignore
        related_webinars = Webinar.manager.get_active_webinars().filter(
            ~Q(grouping_token="")
            & ~Q(id=webinar_id)
            & Q(grouping_token=self.webinar.grouping_token)
        )
        return related_webinars if related_webinars.exists() else []

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
                "Cena i Faktura",
                "core:webinar_price_and_invoice_page",
                "ki-price-tag",
            ),
            (
                "Opinie",
                "core:webinar_opinions_page",
                "ki-like-shapes",
            ),
            (
                "Certyfikat",
                "core:webinar_certificate_page",
                "ki-like-shapes",
            ),
            # (
            #     "Polecja i Zarabiaj",
            #     "core:webinar_loyalty_program_page",
            #     "ki-like-shapes",
            # ),
            # ( # TODO: Finish FAQ
            #     "FAQ",
            #     "core:webinar_faq_page",
            #     "ki-like-shapes",
            # ),
        ]
        _tab_index = tab_index if all([tab_index >= 0, tab_index < len(tabs)]) else 0
        return [
            (
                title,  # tab title
                reverse(url_name, kwargs={"slug": self.webinar.slug}),  # url
                idx == _tab_index,  # is active
                icon,  # icon
            )
            for idx, (title, url_name, icon) in enumerate(tabs)
        ]
