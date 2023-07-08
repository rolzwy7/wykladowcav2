class RedirectException(Exception):
    """Redirect Exception"""

    def __init__(self, url: str):
        self.url = url


class UnauthorizedException(Exception):
    """Unauthorized Exception"""

    def __init__(self):
        pass
