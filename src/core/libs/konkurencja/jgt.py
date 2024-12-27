"""Konkurencja CentrumVerte"""

# flake8: noqa=E501
# pylint: disable=broad-exception-caught

from datetime import datetime

from bs4 import BeautifulSoup, NavigableString
from django.utils.timezone import now

from .abstracts import KonkurencjaFetcher


class JgtFetcher(KonkurencjaFetcher):
    """JgtFetcher"""

    def get_program(self) -> str | None:
        """Retrieve the program details."""
        # Parse the HTML
        soup = BeautifulSoup(self.html_content, "html.parser")

        # Find the div with class 'cke-content'
        try:
            cke_content_div = soup.find_all("div", class_="cke-content")[1]
        except IndexError:
            self.append_log("get_program", "Index error")
            return None

        # Get the inner HTML
        if cke_content_div and not isinstance(cke_content_div, NavigableString):
            inner_html = cke_content_div.decode_contents()  # Extracts inner HTML
            return inner_html

        self.append_log("get_program", "not found cke_content_div")
        return None

    def get_lecturer(self) -> str | None:
        """Retrieve the lecturer's name."""
        return None

    def get_price(self) -> int | None:
        """Retrieve the price of the course."""
        return 999

    def get_date(self) -> datetime | None:
        """Retrieve the course date."""
        return now().replace(hour=10, minute=0, second=0, microsecond=0)

    def get_title(self) -> str | None:
        """Retrieve the course title."""
        ret = self.selector.xpath('//h1[@class="reset-heading"]/text()').get()
        if ret:
            return ret
        else:
            self.append_log("get_title", "Could not get title with xpath")
