"""Normalize webinar program"""

# flake8: noqa=E501
from bs4 import BeautifulSoup
from markdown import markdown
from markdownify import markdownify


def program_remarkdownify(html: str):
    """program_normalize"""
    return markdown(markdownify(html))


def program_normalize(html: str):
    """
    Normalizes all <ul> tags to <ol> and applies styles to a nested HTML
    list to achieve the following:
    - First-level list: numbered (1, 2, 3, ...)
    - Second-level list: alphabetic (a, b, c, ...)
    - Third-level list: dotted

    :param html: A string containing the HTML nested list.
    :return: A string with the styled HTML.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Normalize all <ul> tags to <ol>
    for ul in soup.find_all("ul"):
        ul.name = "ol"

    def apply_styles(ol, level):
        if level == 1:
            ol["style"] = "list-style-type: decimal;"
        elif level == 2:
            ol["style"] = "list-style-type: lower-alpha;"
        elif level == 3:
            ol["style"] = "list-style-type: disc;"

        for li in ol.find_all("li", recursive=False):
            nested_ol = li.find("ol", recursive=False)
            if nested_ol:
                apply_styles(nested_ol, level + 1)

    # Find top-level <ol> elements and apply styles recursively
    for ol in soup.find_all("ol", recursive=False):
        apply_styles(ol, 1)

    return str(soup)


def tabowanie_to_html(tabowanie: str):
    """tabowanie_to_html"""

    def prepend_number_to_lines(text):
        """
        Prepends '1. ' to each line in a text, ignoring leading tabs.

        Args:
            text (str): The input text with lines.

        Returns:
            str: The updated text with '1. ' prepended to each line, respecting leading tabs.
        """
        lines = text.splitlines()
        updated_lines = []

        for line in lines:
            stripped_line = line.lstrip("\t")  # Remove leading tabs temporarily
            if stripped_line:  # Only prepend if there's content
                updated_line = (
                    f"{line[:len(line) - len(stripped_line)]}1. {stripped_line}"
                )
            else:
                updated_line = line  # Keep empty lines or lines with only tabs as is
            updated_lines.append(updated_line)

        return "\n".join(updated_lines)

    return markdown(
        "\n".join(
            [
                prepend_number_to_lines(line)
                for line in tabowanie.split("\n")
                if line.strip() != ""
            ]
        )
    )
