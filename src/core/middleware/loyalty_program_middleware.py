from django.http import HttpRequest

from core.services import ReflinkService


def should_middleware_process_request(request: HttpRequest):
    """Check if this middleware should process request"""
    return not any(
        [
            request.path.startswith("/assets"),
            request.path.startswith("/static"),
            request.path.startswith("/media"),
            request.path.startswith("/css/"),
            request.path.startswith("/js/"),
            request.path.startswith("/plugins/"),
        ]
    )


class LoyaltyProgramMiddleware:
    """Handle `PermissionDeniedRedirect` exception"""

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # This moddleware doesn't need to run on assets/static etc. reqeusts
        if not should_middleware_process_request(request):
            response = self.get_response(request)
            return response

        reflink_service = ReflinkService(request)

        # Delete reflink session data if expired
        ReflinkService.delete_reflink_session_data(request)

        # Set referral number in session
        if reflink_service.is_refcode_valid():
            # Get refcode
            refcode = reflink_service.get_ref_code()
            # Override current `ref` value
            request.session["ref"] = refcode
            # Set `ref_expiration` time
            request.session[
                "ref_expiration"
            ] = ReflinkService.get_reflink_expiration_timestamp()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
