from typing import Any

import html2text
from django.template.loader import get_template

from .email_common_context import get_email_common_context


class EmailTemplate:
    """Represents email template"""

    def __init__(self, template_path: str, context: dict[str, Any]) -> None:
        self.template_path = template_path
        self.template = get_template(template_path)
        self.context = {**context, **get_email_common_context()}

    def update_context(self, context: dict[str, Any]):
        """Update context"""
        self.context = {**self.context, **context}

    def get_html(self):
        """Get HTML template"""
        return self.template.render(self.context)

    def get_text(self):
        """Get TEXT template"""
        h2t = html2text.HTML2Text()
        return h2t.handle(self.get_html())

    @staticmethod
    def html2text(html: str):
        """Converts HTML to TEXT"""
        h2t = html2text.HTML2Text()
        return h2t.handle(html)
