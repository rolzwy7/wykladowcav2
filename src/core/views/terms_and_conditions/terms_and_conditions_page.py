from django.template.response import TemplateResponse


def terms_and_conditions_webinars(request):
    """Term and conditions for webinars"""
    template_name = (
        "geeks/pages/terms_and_conditions/TermsAndConditionsWebinars.html"
    )
    return TemplateResponse(
        request,
        template_name,
        {},
    )


def terms_and_conditions_loyalty_program(request):
    """Term and conditions for webinars"""
    template_name = (
        "geeks/pages/terms_and_conditions/TermsAndConditionsLoyaltyProgram.html"
    )
    return TemplateResponse(
        request,
        template_name,
        {},
    )


def cookies_policy(request):
    """Term and conditions for webinars"""
    template_name = "geeks/pages/terms_and_conditions/CookiesPolicy.html"
    return TemplateResponse(
        request,
        template_name,
        {},
    )


def privacy_policy(request):
    """Term and conditions for webinars"""
    template_name = "geeks/pages/terms_and_conditions/PrivacyPolicy.html"
    return TemplateResponse(
        request,
        template_name,
        {},
    )
