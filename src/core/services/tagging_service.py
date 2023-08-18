import re

import requests


class TaggingService:
    """Tagging service"""

    EMAIL_REGEXP = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

    def __init__(self) -> None:
        pass

    def get_response(self, url: str):
        """Get response"""
        return requests.get(url, timeout=(10, 10))

    def download_page(self, url: str):
        """Download page"""
        response = self.get_response(url)
        if response.ok:
            return (response.ok, response.status_code, response.content)
        return (response.ok, response.status_code, b"")

    def find_all_emails(self, content: str) -> list[str]:
        """Find all emails"""
        return list(set(re.findall(self.EMAIL_REGEXP, content)))
