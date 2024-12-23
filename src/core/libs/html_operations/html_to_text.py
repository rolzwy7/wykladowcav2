"""HTML op html to text"""

from html2text import HTML2Text


def html_to_text(html: str) -> str:
    """Create text version from HTML"""
    html2text = HTML2Text()
    return html2text.handle(html)
