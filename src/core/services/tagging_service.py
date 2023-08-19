import re

import requests
from django.core.files.uploadedfile import InMemoryUploadedFile

from core.models.tagging import TaggedEmailManager


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

    def load_emails_from_file_into_tagging(
        self, file: InMemoryUploadedFile, tag: str
    ) -> None:
        """Load emails from file into campaign"""

        manager = TaggedEmailManager()
        # batch = []

        for line in file:
            if isinstance(line, str):
                email = line.strip().lower()
            else:
                email = str(line, "utf8").strip().lower()

            if re.match(self.EMAIL_REGEXP, email) is None:
                continue

            manager.get_or_create_tagged_email(email)
            # TODO: if tag already in then skip
            manager.add_tags_to_email(email, [tag])

            # batch.append(manager.create_upsert_object(email, [tag]))

            # if len(batch) >= 100:
            #     manager.collection.bulk_write(batch)
            #     batch = []

        # if batch:
        #     manager.collection.bulk_write(batch)
        #     batch = []

        manager.close()
