import re
from time import time

from django.conf import settings
from django.http import HttpRequest


class LoyaltyProgramMiddleware:
    """Handle `PermissionDeniedRedirect` exception"""

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # This moddleware doesn't need to run on assets/static etc. reqeusts
        if any(
            [
                request.path.startswith("/assets"),
                request.path.startswith("/static"),
                request.path.startswith("/media"),
                request.path.startswith("/css/"),
                request.path.startswith("/js/"),
                request.path.startswith("/plugins/"),
            ]
        ):
            response = self.get_response(request)
            return response

        # Delete `ref*` session keys if expired
        if request.session.get("ref_expiration"):
            if int(time()) > request.session["ref_expiration"]:
                for key_delete in ["ref", "ref_expiration"]:
                    try:
                        del request.session[key_delete]
                    except KeyError:
                        pass

        # Set referral number in session
        if all(
            [
                # `ref` GET key is set
                request.GET.get("ref") is not None,
                # `ref` GET key is digits (5 to 15 in length)
                re.match(r"[0-9]{5,15}", request.GET.get("ref", "")),
            ]
        ):
            # Override current `ref` value
            request.session["ref"] = request.GET["ref"]
            # Set `ref_expiration` time
            request.session["ref_expiration"] = (
                int(time()) + settings.LOYALTY_PROGRAM_REF_EXPIRATION_SECONDS
            )

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
