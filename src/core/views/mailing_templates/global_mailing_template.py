"""
Mailing template
"""

# flake8: noqa=E501

from random import shuffle

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from markdown import markdown

from core.consts.spamphrases_consts import SPAM_PHRASES
from core.models import Lecturer, Webinar, WebinarCategory

BASE_URL = settings.BASE_URL


def split_pairs(seq):
    """Split pairs"""
    ret = []
    for i in range(0, len(seq) + 1, 2):
        ret.append(seq[i : i + 2])
    return ret


def global_mailing_template_page(request):
    """Mailing template for webinar category"""

    # TODO:
    # webinar_for = request.GET.get("webinar_for")
    # patron_section = request.GET.get("patron_section")
    # promo_code = request.GET.get("promo_code")
    # promo_text = request.GET.get("promo_text")
    # promo_value = request.GET.get("promo_value")
    # show_last_spots = request.GET.get("show_last_spots")
    # show_price = request.GET.get("show_price")
    # show_logo = request.GET.get("show_logo")

    controls = {
        "show_last_spots": request.GET.get("show_last_spots"),
        "show_price": request.GET.get("show_price"),
        "section_fb_group": request.GET.get("section_fb_group"),
        "section_loyalty": request.GET.get("section_loyalty"),
        "lecturer_section": request.GET.get("lecturer_section"),
        "background_color": "#f1f4fa",
        "max_width": "640px",
    }

    template_name = "mailing_templates/GlobalMailingTemplate.html"
    all_webinars = []
    category_webinars = []
    lecturer_webinars = []
    subcategories_pairs = []
    main_webinar = None
    lecturer = None
    webinars_map = {}
    cta_href = ""
    cta_text = ""
    program = ""

    # Webinar
    webinar_id = request.GET.get("webinar_id")
    if webinar_id:
        main_webinar = get_object_or_404(Webinar, pk=int(webinar_id))
        lecturer = main_webinar.lecturer
        webpath = reverse(
            "core:webinar_redirect_to_program", kwargs={"pk": int(webinar_id)}
        )
        cta_href = f"{BASE_URL}{webpath}"
        cta_text = "Zapisz się teraz!"

        _program = markdown(main_webinar.program_markdown)

        program: str = _program
        for original, replacement in SPAM_PHRASES.items():
            program = program.replace(original, replacement)
            program = program.replace(original.upper(), replacement)
            program = program.replace(original.capitalize(), replacement)

    # Category webinars
    category_slug = request.GET.get("category_slug")
    if category_slug:
        if category_slug == "wszystkie-szkolenia":
            subcategories = WebinarCategory.manager.get_visible_categories()
        else:
            main_category = get_object_or_404(WebinarCategory, slug=category_slug)
            subcategories = WebinarCategory.manager.get_subcategories(main_category)
        all_slugs = [category_slug, *[_.slug for _ in subcategories]]
        # Get all webinars for main category and subcatagories
        category_webinars = Webinar.manager.get_active_webinars_for_category_slugs(
            all_slugs
        )
        subcategories_pairs = split_pairs(subcategories)

    # Lecturer webinars
    lecturer_slug = request.GET.get("lecturer_slug")
    if lecturer_slug:
        lecturer = Lecturer.manager.get(slug=lecturer_slug)
        lecturer_webinars = Webinar.manager.get_active_webinars_for_lecturer(
            lecturer.id
        )

    for webinar in category_webinars:
        if webinar not in all_webinars:
            all_webinars.append(webinar)

    for webinar in lecturer_webinars:
        if webinar not in all_webinars:
            all_webinars.append(webinar)

    # Create keys for durations
    for _ in all_webinars:
        webinars_map[_.get_duration_display()] = []  # type: ignore
    # Fill duration lists with webinars
    for _ in all_webinars:
        webinars_map[_.get_duration_display()].append(_)  # type: ignore
    # Make webinar pairs
    for key, value in webinars_map.items():
        webinars_map[key] = split_pairs(value)

    td_classes = [
        "border-collapse:collapse;",
        "padding-left:20px;",
        "padding-right:20px;",
        "font-size: 16px;",
    ]
    shuffle(td_classes)

    return TemplateResponse(
        request,
        template_name,
        {
            "main_webinar": main_webinar,
            "lecturer": lecturer,
            "webinars_map": webinars_map,
            "subcategories_pairs": subcategories_pairs,
            "BASE_URL": BASE_URL,
            "td_classes": "".join(td_classes),
            "cta_href": cta_href,
            "cta_text": cta_text,
            "program": program,
            **controls,
        },
    )
