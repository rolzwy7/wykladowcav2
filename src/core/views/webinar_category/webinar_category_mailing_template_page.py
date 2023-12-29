"""
Webinar ctegory template page
"""

# flake8: noqa

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from core.models import Webinar, WebinarCategory

BASE_URL = settings.BASE_URL


def webinar_category_mailing_template_page(request, slug: str):
    """Mailing template for webinar category"""

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
        "mailing_templates/MailingWebinarCategoryList/WebinarCategoryMailingTemplatePage.html",
        {
            "background_color": "#f1f4fa",
            "max_width": "640px",
            "webinars_map": ctx,
            "subcategories": [s for s in subcategories][:4],
            "BASE_URL": BASE_URL,
        },
    )
