"""Konkurencja CentrumVerte"""

# flake8: noqa=E501
# pylint: disable=broad-exception-caught

from datetime import datetime

from bs4 import BeautifulSoup, NavigableString

from .abstracts import KonkurencjaFetcher


class CentrumVerteFetcher(KonkurencjaFetcher):
    """CentrumVerteFetcher"""

    def get_program(self) -> str | None:
        """Retrieve the program details."""

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(self.html_content, "html.parser")

        # Find the div with class 'program-desc'
        program_desc_div = soup.find("div", class_="program-desc")

        lis: list[str] = []

        # If the div is found, proceed with further processing
        if program_desc_div and not isinstance(program_desc_div, NavigableString):
            # Find all div elements with class 'item' inside the 'program-desc' div
            item_divs = program_desc_div.find_all("div", class_="item")

            # Iterate over each div.item
            for item in item_divs:
                # Get the text inside the h3 tag
                h3_text: str | None = (
                    item.find("h3").get_text(strip=True) if item.find("h3") else None
                )
                if not h3_text:
                    continue

                try:
                    h3_text = h3_text.split(".", 1)[1].strip()
                except Exception as e:  # not list-like h3
                    continue

                # Get the HTML of the ul tag
                ul_html: str | None = str(item.find("ul")) if item.find("ul") else None
                if not ul_html:
                    ul_html = ""

                # Print or store the extracted data
                print("H3 Text:", h3_text)
                print("UL HTML:", ul_html)
                print("-" * 30)

                lis.append(f"<li>{h3_text} {ul_html}</li>")

            return "\n".join(
                [
                    "<ol>",
                    *lis,
                    "</ol>",
                ]
            )

    def get_lecturer(self) -> str | None:
        """Retrieve the lecturer's name."""
        ret = self.selector.xpath(
            '//*[@id="single-course-page"]/div/div[1]/div[5]/div/p[2]/a/text()'
        ).get()
        if ret:
            return ret
        else:
            self.append_log("get_lecturer", "Could not get lecturer with xpath")

    def get_price(self) -> int | None:
        """Retrieve the price of the course."""
        ret = self.selector.xpath('//*[@id="price"]/text()').get()
        if ret:
            try:
                return int(ret.split("zł")[0].strip())
            except Exception as e:
                self.append_log("get_price", "Could parse price to int")
                self.append_log("get_price", f"{e}")
                return
        else:
            self.append_log("get_price", "Could not get price with xpath")

    def get_date(self) -> datetime | None:
        """Retrieve the course date."""
        ret = self.selector.xpath(
            '//*[@id="single-course-page"]/div/div[1]/div[1]/div/div[1]/ul/li/text()'
        ).getall()
        if ret:
            joined_ret = " ".join(ret).strip()
            self.append_log("get_date", f"Got `{joined_ret}`")
            try:
                datetime_str_cleaned = joined_ret.replace("r. godz. ", ".").strip(".")
                datetime_format = "%d.%m.%Y.%H.%M"
                return datetime.strptime(datetime_str_cleaned, datetime_format)
            except Exception as e:
                self.append_log("get_date", "Could not parse date to datetime")
                self.append_log("get_date", f"{e}")
        else:
            self.append_log("get_date", "Could not get date with xpath")

    def get_title(self) -> str | None:
        """Retrieve the course title."""
        ret = self.selector.xpath('//*[@id="szkolenie_nazwa"]/text()').get()
        if ret:
            return ret
        else:
            self.append_log("get_title", "Could not get title with xpath")
