class RedirectException(Exception):
    """Redirect Exception"""

    def __init__(self, url: str):
        self.url = url
        self.message = "Redirecting exception"
        super().__init__(self.message)


class UnauthorizedException(Exception):
    """Unauthorized Exception"""

    def __init__(self):
        self.message = "Unauthorized access exception"
        super().__init__(self.message)


class ClickmeetingError(Exception):
    """Unauthorized Exception"""

    def __init__(self, message: str):
        """Init

        Args:
            response_dump (str): json response dump
            room_id (str): room id
        """
        self.message = message
        super().__init__(self.message)
