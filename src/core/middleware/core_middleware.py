from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.exceptions import RedirectException, UnauthorizedException
from core.permissions import deny_if_not_staff
from core.utils.redirects import manual_redirect


class CoreMiddleware:
    """Handle `PermissionDeniedRedirect` exception"""

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Deny access to CRM for unauthenticated users and
        # users that are authenticated but aren't staff memebers
        if request.path.startswith("/crm/"):
            try:
                deny_if_not_staff(request.user)
            except UnauthorizedException:
                return HttpResponse(
                    'Brak dostępu. <a href="/cms/">Zaloguj się</a>', status=401
                )

        # Calling view
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        # If response is 404 try to find and return manual redirect
        if response.status_code == 404:
            redirect_response = manual_redirect(request.path)
            if redirect_response:
                return redirect_response

        return response

    def process_exception(self, request, exception):
        """Process exception"""
        if isinstance(exception, RedirectException):
            return redirect(exception.url)

        elif isinstance(exception, UnauthorizedException):
            return HttpResponse("Unauthorized", status=401)
