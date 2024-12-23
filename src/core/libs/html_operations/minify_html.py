"""HTML op minify html"""

import minify_html


def op_minify_html(html: str) -> str:
    """Minify HTML"""

    return minify_html.minify(  # pylint: disable=no-member
        html, minify_js=True, remove_processing_instructions=True
    )
