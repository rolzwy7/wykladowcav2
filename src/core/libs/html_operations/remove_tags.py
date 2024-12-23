"""HTML op remove tags"""

from bs4 import BeautifulSoup


def remove_tags(html: str, tags: list[str]) -> str:
    """Remove style tags from HTML"""

    # Parse the HTML
    soup = BeautifulSoup(html, "lxml")

    # Remove all <style> tags
    for tag in tags:
        for style_tag in soup(tag):
            style_tag.decompose()

    return str(soup)
