import re
from time import time

from django.conf import settings
from django.http import HttpRequest


class ReflinkService:
    """Referral link service"""

    def __init__(self, request: HttpRequest) -> None:
        self.request = request

    def is_refcode_valid(self) -> bool:  # TODO: test this
        """Check if refcode is valid"""
        if not self.is_refcode_in_get_params():
            return False

        return not (re.match(r"[0-9]{5,15}", self.get_ref_code()) is None)

    def is_refcode_in_get_params(self) -> bool:
        """Check if refcode is in GET params"""
        return not (self.request.GET.get("ref") is None)

    def get_ref_code(self) -> str:
        """Get refcode from GET params

        Returns:
            str: _description_

        Raises:
            KeyError: When `ref` GET param is not set
        """
        return self.request.GET["ref"]

    @staticmethod
    def get_reflink_expiration_timestamp() -> int:
        """Get timestamp representing expiration time of reflink"""
        return int(time()) + settings.LOYALTY_PROGRAM_REF_EXPIRATION_SECONDS

    @staticmethod
    def delete_reflink_session_data(request: HttpRequest):
        """Delete session keys associated with reflink handling"""

        if request.session.get("ref_expiration"):
            if int(time()) > request.session["ref_expiration"]:
                for key_delete in ["ref", "ref_expiration"]:
                    try:
                        del request.session[key_delete]
                    except KeyError:
                        pass
