"""
Mailing template category
"""

# flake8: noqa

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar, WebinarCategory


def webinar_category_mailing_editor_page(request, slug: str):
    """Mailing editor page for webinar category"""

    template_name = "mailing_templates/WebinarCategoryMailingEditor.html"
    return TemplateResponse(
        request,
        template_name,
        {"slug": slug},
    )


def webinar_category_mailing_template_page(request, slug: str):
    """Mailing template for webinar category"""

    template_name = "mailing_templates/WebinarCategoryMailingTemplate.html"

    if slug == "wszystkie-szkolenia":
        subcategories = WebinarCategory.manager.get_visible_categories()
    else:
        main_category = get_object_or_404(WebinarCategory, slug=slug)
        subcategories = WebinarCategory.manager.get_subcategories(main_category)

    all_slugs = [slug, *[_.slug for _ in subcategories]]

    # Get all webinars for main category and subcatagories
    webinars = list(Webinar.manager.get_active_webinars_for_category_slugs(all_slugs))

    ctx = {}

    def _split_pairs(seq):
        ret = []
        for i in range(0, len(seq) + 1, 2):
            ret.append(seq[i : i + 2])
        return ret

    # Create keys for durations
    for _ in webinars:
        ctx[_.get_duration_display()] = []  # type: ignore

    for _ in webinars:
        ctx[_.get_duration_display()].append(_)  # type: ignore

    for key, value in ctx.items():
        ctx[key] = _split_pairs(value)

    return TemplateResponse(
        request,
        template_name,
        {
            "background_color": "#f1f4fa",
            "max_width": "640px",
            "webinars_map": ctx,
            "subcategories_pairs": _split_pairs(subcategories),
            "BASE_URL": settings.BASE_URL,
        },
    )
