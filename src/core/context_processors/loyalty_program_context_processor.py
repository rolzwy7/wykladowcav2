from django.http import HttpRequest


def loyalty_program(request: HttpRequest):
    """Loyalty program context processor"""
    return {"ACTIVE_REFCODE": request.session.get("ref")}
