""""""

# flake8: noqa=E501
# pylint: disable=line-too-long

from abc import ABC, abstractmethod
from datetime import datetime

import requests
from scrapy import Selector

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"


class KonkurencjaFetcher(ABC):
    """KonkurencjaFetcher"""

    def __init__(self, url: str):
        self.url = url
        self.logs: list[str] = []
        self.html_content = ""
        self.selector = Selector(text="")

    def append_log(self, method: str, line: str):
        """append log"""
        log_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(f"[{log_timestamp}][{method}] {line}")

    def fetch_get(self, url: str, timeout: int = 3) -> tuple[bool, str]:
        """Fetch url html content"""
        try:
            response = requests.get(self.url, timeout=10, headers={"User-Agent": UA})
        except Exception as e:
            self.append_log("fetch_get", str(e))
            return False, ""
        else:
            html_content = response.text
            return True, html_content

    def initialize(self):
        """initialize fetcher"""

        content = "not_fetched"
        retries = 3
        for retry in range(retries):
            self.append_log("initialize", f"Try to fetch url {retry+1}/{retries}")
            success, html_content = self.fetch_get(self.url, timeout=(retry + 1) * 4)
            if success:
                self.append_log("initialize", "Try to fetch url SUCCESS")
                content = html_content
                break
            else:
                self.append_log("initialize", "Try to fetch url fail")

        if content == "not_fetched":
            self.append_log("initialize", f"Could not fetch after {retries} retries")
            raise RuntimeError("Fetcher failed")

        self.html_content = content
        self.selector = Selector(text=content)

    @abstractmethod
    def get_program(self) -> str | None:
        """Retrieve the program details."""
        pass

    @abstractmethod
    def get_lecturer(self) -> str | None:
        """Retrieve the lecturer's name."""
        pass

    @abstractmethod
    def get_price(self) -> int | None:
        """Retrieve the price of the course."""
        pass

    @abstractmethod
    def get_date(self) -> datetime | None:
        """Retrieve the course date."""
        pass

    @abstractmethod
    def get_title(self) -> str | None:
        """Retrieve the course title."""
        pass
