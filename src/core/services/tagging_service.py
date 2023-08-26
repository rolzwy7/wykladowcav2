import re

import requests
from django.core.files.uploadedfile import InMemoryUploadedFile

from core.consts import WEBMAILS
from core.models.tagging import TaggedEmailManager


class TaggingService:
    """Tagging service"""

    EMAIL_REGEXP = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    DOMAIN_REGEXP = r"[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

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
        self, file: InMemoryUploadedFile, tag: str, remove_tags: bool = False
    ) -> None:
        """Load emails, add tag or remove tag"""

        manager = TaggedEmailManager()

        for line in file:
            if isinstance(line, str):
                email = line.strip().lower()
            else:
                email = str(line, "utf8").strip().lower()

            if re.match(self.EMAIL_REGEXP, email) is None:
                continue

            document = manager.get_or_create_tagged_email(email)

            if remove_tags:
                # Skip if email is tagged with provided tag
                if document and tag not in document["tags"]:
                    continue
                else:
                    # Remove tag
                    manager.delete_tags_from_email(email, [tag])
            else:
                # Skip if email is already tagged with provided tag
                if document and tag in document["tags"]:
                    continue
                else:
                    # Add new tag
                    manager.add_tags_to_email(email, [tag])

        manager.close()

    def load_file_tag_emails_by_domain(
        self, file: InMemoryUploadedFile, tag: str, remove_tags: bool = False
    ) -> None:
        """Load domains, add tag or remove tag"""

        manager = TaggedEmailManager()

        for line in file:
            if isinstance(line, str):
                candid = line.strip().lower()
            else:
                candid = str(line, "utf8").strip().lower()

            # Provided e-mail in place of a domain, get domain
            if re.match(self.EMAIL_REGEXP, candid):
                _, domain = candid.split("@")
            else:
                domain = candid

            if re.match(self.DOMAIN_REGEXP, domain) is None:
                continue

            if WEBMAILS.get(domain):
                continue

            new_tag = f"BY-DOMAIN-{tag}"

            if remove_tags:
                manager.delete_tags_from_emails_with_domain(domain, [new_tag])
            else:
                manager.add_tags_to_emails_with_domain(domain, [new_tag])

        manager.close()
