"""Mailing template model"""

# flake8: noqa=E501

import minify_html
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from django.db.models import CharField, Model, TextField
from html2text import HTML2Text

from core.consts.spamphrases_consts import SPAM_PHRASES


class MailingTemplate(Model):
    """Represents mailing template"""

    name = CharField("Nazwa szablonu", max_length=100)
    html = TextField("HTML")
    text = TextField("TEXT", blank=True)

    class Meta:
        verbose_name = "Szablon mailingowy"
        verbose_name_plural = "Szablony mailingowe"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs) -> None:
        # Create text version of email template
        if not self.text:
            self.replace_all_caps_words()
            self.remove_all_tags(["style", "script"])
            self.replace_spam_words_in_body()
            self.minify_html()
            self.create_text_version_from_html()
        return super().save(*args, **kwargs)

    def create_text_version_from_html(self):
        """Create text version from HTML"""
        html2text = HTML2Text()
        self.text = html2text.handle(self.html)

    def remove_all_tags(self, tags: list[str]):
        """Remove style tags from HTML"""

        # Parse the HTML
        soup = BeautifulSoup(self.html, "lxml")

        # Remove all <style> tags
        for tag in tags:
            for style_tag in soup(tag):
                style_tag.decompose()

        self.html = str(soup)

    def minify_html(self):
        """Minify HTML"""

        self.html = minify_html.minify(  # pylint: disable=no-member
            self.html, minify_js=True, remove_processing_instructions=True
        )

    def replace_spam_words_in_body(self):
        """Replace spam words in body"""

        soup = BeautifulSoup(self.html, "lxml")

        body = soup.find("body")

        if not body or not isinstance(body, Tag):
            return

        for tag in body.find_all(recursive=True):
            if not isinstance(tag, Tag):
                continue
            if not isinstance(tag.string, NavigableString):
                continue

            _string = str(tag.string)

            for original, replacement in SPAM_PHRASES.items():

                # replace lower
                if original.lower() in _string:
                    tag.string.replace_with(
                        _string.replace(original.lower(), replacement.lower())
                    )

                # replace upper
                if original.upper() in _string:
                    tag.string.replace_with(
                        _string.replace(original.upper(), replacement.upper())
                    )

                # replace capitalized
                if original.capitalize() in _string:
                    tag.string.replace_with(
                        _string.replace(original.capitalize(), replacement.capitalize())
                    )

        self.html = str(soup)

    def replace_all_caps_words(self):
        """Replace words that are all caps with capitalized version"""

        soup = BeautifulSoup(self.html, "lxml")

        body = soup.find("body")

        if not body or not isinstance(body, Tag):
            return

        for tag in body.find_all(recursive=True):
            if not isinstance(tag, Tag):
                continue
            if not isinstance(tag.string, NavigableString):
                continue

            _string = str(tag.string)

            words = _string.split(" ")
            seq: list[str] = []
            for word in words:
                if word.isupper() and len(word) >= 5:
                    seq.append(word.capitalize())
                else:
                    seq.append(word)

            tag.string.replace_with(" ".join(seq))

        self.html = str(soup)
