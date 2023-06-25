from rest_framework.throttling import SimpleRateThrottle


class RegonAutocompleteThrottle(SimpleRateThrottle):
    rate = "10/minute"

    def get_cache_key(self, request, view):
        """
        Should return a unique cache-key which can be used for throttling.
        Must be overridden.

        May return `None` if the request should not be throttled.
        """

        view_name = view.__class__.__name__
        ip_address = request.META.get("REMOTE_ADDR")

        if not ip_address:
            return None

        return f"{view_name}:{ip_address}"
