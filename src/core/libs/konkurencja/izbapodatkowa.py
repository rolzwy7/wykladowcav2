"""Konkurencja CentrumVerte"""

# flake8: noqa=E501
# pylint: disable=broad-exception-caught

from datetime import datetime

from bs4 import BeautifulSoup, NavigableString
from django.utils.timezone import now

from .abstracts import KonkurencjaFetcher


class IzbaPodatkowaFetcher(KonkurencjaFetcher):
    """IzbaPodatkowaFetcher"""

    def get_program(self) -> str | None:
        """Retrieve the program details."""
        # Parse the HTML
        soup = BeautifulSoup(self.html_content, "html.parser")

        # Find the div with class 'cke-content'
        program_div = soup.find("div", class_="training-program-content")

        # Get the inner HTML
        if program_div and not isinstance(program_div, NavigableString):
            inner_html = program_div.decode_contents()  # Extracts inner HTML
            return inner_html
        else:
            return None

    def get_lecturer(self) -> str | None:
        """Retrieve the lecturer's name."""
        return None

    def get_price(self) -> int | None:
        """Retrieve the price of the course."""
        ret = self.selector.xpath('//*[@id="termin-price"]/text()').get()
        if ret:
            try:
                return int("".join([ch for ch in ret if ch.isdigit()]))
            except Exception as e:
                self.append_log("get_price", "Could parse price to int")
                self.append_log("get_price", f"{e}")
                return
        else:
            self.append_log("get_price", "Could not get price with xpath")

    def get_date(self) -> datetime | None:
        """Retrieve the course date."""
        return now().replace(hour=10, minute=0, second=0, microsecond=0)

    def get_title(self) -> str | None:
        """Retrieve the course title."""
        ret = self.selector.xpath('//*[@id="page-content"]/div[1]/div/h1/text()').get()
        if ret:
            return ret
        else:
            self.append_log("get_title", "Could not get title with xpath")
