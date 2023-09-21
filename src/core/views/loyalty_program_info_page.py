from django.template.response import TemplateResponse


def loyalty_program_info_page(request):
    """Loyalty Program Info Page"""
    template_path = "geeks/pages/LoyaltyProgramInfoPage.html"
    return TemplateResponse(request, template_path, {})
