import markdown


class ProgramService:
    """Program service"""

    def __init__(self, program_markdown: str) -> None:
        self.program_markdown = program_markdown

    def get_enriched(self):
        """Get enriched program version"""
        html = markdown.markdown(self.program_markdown)

        return html
