class AntispamService:
    """Anti-Spam service"""

    def __init__(self, content: str):
        self.original_content = content
        self.content_lower = content.lower()

    @staticmethod  # TODO
    def calculate_text_html_ratio(html: str, text: str) -> float:
        """Calculate ratio between lengths of text and html content"""
        if len(html) == 0:
            return -1
        return round(len(text) / len(html), 2)

    def detect_spam_phrases(self):  # TODO: detect_spam_phrases
        """Detect spam phrases in content"""
        pass

    def calculate_spam_pharse_score(self):  # TODO: calculate
        """Calculate spam score for content"""
        pass

    def html_replace_spam_phrases(self):  # TODO: html_replace_spam_phrases
        """Replace spam phrases in HTML with replacements"""
        pass
