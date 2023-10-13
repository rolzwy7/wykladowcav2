from typing import Dict

from django.http import HttpRequest


class IpAddressService:
    """IP address service"""

    @staticmethod
    def get_client_ip(request: HttpRequest) -> str:
        """Get client IP address"""
        meta: Dict[str, str] = request.META
        x_forwarded_for: str = meta.get("HTTP_X_FORWARDED_FOR", "")
        if x_forwarded_for:
            try:
                return x_forwarded_for.split(",")[0]
            except IndexError:
                return "IndexError"
        else:
            # Otherwise, use the REMOTE_ADDR from META
            ip_address: str = meta.get("REMOTE_ADDR", "")
            return ip_address
