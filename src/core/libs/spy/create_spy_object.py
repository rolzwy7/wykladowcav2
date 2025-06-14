from core.models import SpyObject
from core.services import IpAddressService


def create_spy_object(
    request,
    source: str,
    param_a: str = "",
    param_b: str = "",
    param_c: str = "",
    google_recaptcha_v3: float = -1.0,
):
    """create_spy_object"""

    session_key = request.session.session_key

    spy_object = SpyObject(
        source=source,
        param_a=param_a,
        param_b=param_b,
        param_c=param_c,
        ip_address=IpAddressService.get_client_ip(request),
        session_key=session_key if session_key else "",
        tracking_code=request.session.get("tracking_code", "no_code"),
        campaign_id=request.session.get("campaign_id", "no_campaign_id"),
        fingerprint=request.session.get("fingerprint", "no_fingerprint"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
        logged_in=request.user.is_authenticated,
        user_id=str(request.user.id) if request.user.is_authenticated else "",
        google_recaptcha_v3=google_recaptcha_v3,
    )

    spy_object.save()

    return spy_object
