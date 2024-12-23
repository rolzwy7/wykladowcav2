"""Mailing template model"""

# flake8: noqa=E501

import minify_html
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from django.db.models import CharField, Model, TextField
from html2text import HTML2Text

from core.consts.spamphrases_consts import SPAM_PHRASES
from core.libs.html_operations.html_text_replacer import (
    ANTISPAM_REPLACEMENTS_MAP,
    HTMLTextReplacer,
)
from core.libs.html_operations.html_to_text import html_to_text
from core.libs.html_operations.minify_html import op_minify_html
from core.libs.html_operations.remove_tags import remove_tags


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
            # HTML
            self.html = remove_tags(self.html, ["style", "script"])
            html_replacer = HTMLTextReplacer(ANTISPAM_REPLACEMENTS_MAP)
            self.html = html_replacer.replace_text(self.html)
            self.html = op_minify_html(self.html)
            # TEXT
            self.text = html_to_text(self.html)
        return super().save(*args, **kwargs)
