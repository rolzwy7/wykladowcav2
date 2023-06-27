from typing import Any

import html2text
from django.template.loader import get_template


class EmailTemplate:
    """Represents email template"""

    def __init__(self, template_path: str, context: dict[str, Any]) -> None:
        self.template_path = template_path
        self.template = get_template(template_path)
        self.html = self.template.render(context)
        self.text = self.html2text(self.html)

    @staticmethod
    def html2text(html: str):
        """Converts HTML to TEXT"""
        return html2text.HTML2Text().handle(html)
