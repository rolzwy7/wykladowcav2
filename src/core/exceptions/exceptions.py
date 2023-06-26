class RedirectException(Exception):
    """Instead of showing 5xx page it redirects user to given URL"""

    def __init__(self, url: str):
        self.url = url
