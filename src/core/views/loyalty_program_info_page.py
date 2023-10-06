from django.shortcuts import redirect
from django.template.response import TemplateResponse


def loyalty_program_info_page(request):
    """Loyalty Program Info Page"""
    template_path = "geeks/pages/LoyaltyProgramInfoPage.html"
    return TemplateResponse(request, template_path, {})


def loyalty_program_video_page(request):
    """Loyalty Program Video Page"""
    return redirect("https://www.youtube.com/watch?v=WQg_HnpS-jE")
    # template_path = "geeks/pages/LoyaltyProgramVideoPage.html"
    # return TemplateResponse(request, template_path, {})
