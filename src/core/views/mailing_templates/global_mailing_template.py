"""
Mailing template
"""

# flake8: noqa=E501

from random import shuffle

from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import now, timedelta
from markdown import markdown

from core.models import (
    Lecturer,
    ServiceOffer,
    Webinar,
    WebinarAggregate,
    WebinarCategory,
)
from core.services.webinar import WebinarService

BASE_URL = settings.BASE_URL


def split_pairs(seq):
    """Split pairs"""
    ret = []
    for i in range(0, len(seq) + 1, 2):
        ret.append(seq[i : i + 2])
    return ret


def global_mailing_editor_page(request):
    """Email editor page"""

    for_webinar_id = request.GET.get("for_webinar_id")
    category_slug = request.GET.get("for_category_slug")
    lecturer_slug = request.GET.get("for_lecturer_slug")
    for_service_offer_id = request.GET.get("for_service_offer_id")
    for_short_service_offer_id = request.GET.get("short_service_offer_id")
    categories = WebinarCategory.manager.get_visible_categories()
    service_offers = ServiceOffer.manager.all()
    lecturers = Lecturer.manager.all()

    params_seq = []
    if for_webinar_id:
        params_seq.append(f"for_webinar_id={for_webinar_id}")
    if category_slug:
        params_seq.append(f"for_category_slug={category_slug}")
    if lecturer_slug:
        params_seq.append(f"for_lecturer_slug={lecturer_slug}")
    if for_service_offer_id:
        params_seq.append(f"for_service_offer_id={for_service_offer_id}")
    if for_short_service_offer_id:
        params_seq.append(f"short_service_offer_id={for_short_service_offer_id}")
    params_str = "&".join(params_seq)

    try:
        webinar: Webinar = Webinar.manager.get(pk=for_webinar_id)
        webinar_id = webinar.id  # type: ignore
        less_than_week_webinar = now() > webinar.date - timedelta(days=7)
    except Webinar.DoesNotExist:  # pylint: disable=no-member
        webinar = None  # type: ignore
        webinar_id = None
        less_than_week_webinar = False

    try:
        service_offer = ServiceOffer.manager.get(pk=for_service_offer_id)
        service_offer_id = service_offer.id
    except ServiceOffer.DoesNotExist:  # pylint: disable=no-member
        service_offer = None
        service_offer_id = None

    try:
        short_service_offer = ServiceOffer.manager.get(pk=for_short_service_offer_id)
        short_service_offer_id = short_service_offer.id
    except ServiceOffer.DoesNotExist:  # pylint: disable=no-member
        short_service_offer = None
        short_service_offer_id = None

    template_name = "mailing_templates/GlobalMailingEditor.html"
    return TemplateResponse(
        request,
        template_name,
        {
            "params_str": params_str,
            "lecturers": lecturers,
            "categories": categories,
            "webinar": webinar,
            "webinar_id": webinar_id,
            "lecturer_slug": lecturer_slug,
            "category_slug": category_slug,
            "service_offers": service_offers,
            "service_offer": service_offer,
            "service_offer_id": service_offer_id,
            "short_service_offer": short_service_offer,
            "short_service_offer_id": short_service_offer_id,
            "less_than_week_webinar": less_than_week_webinar,
            "closed_webinar_btn_url": settings.BASE_URL
            + reverse("core:closed_webinar_contact_page"),
        },
    )


def global_mailing_template_page(request):
    """Mailing template for webinar category"""

    controls = {
        "hide_head_tag": True,
        "access_to_recordings": request.GET.get("access_to_recordings"),
        "promo_code": request.GET.get("promo_code"),
        "promo_value": request.GET.get("promo_value"),
        "for_whom": request.GET.get("for_whom"),
        "show_logo": request.GET.get("show_logo"),
        "show_last_spots": request.GET.get("show_last_spots"),
        "show_price": request.GET.get("show_price"),
        "pewny_termin": request.GET.get("pewny_termin"),
        "show_hello_text": request.GET.get("show_hello_text"),
        "section_fb_group": request.GET.get("section_fb_group"),
        "section_loyalty": request.GET.get("section_loyalty"),
        "button_closed_webinar": request.GET.get("button_closed_webinar"),
        "button_buy_recording": request.GET.get("button_buy_recording"),
        "lecturer_section": request.GET.get("lecturer_section"),
        "patron_section": request.GET.get("patron_section"),
        "other_cat_section": request.GET.get("other_cat_section"),
        "background_color": "#f1f4fa",
        "max_width": "640px",
        "subject_override": request.GET.get("subject_override"),
        "closed_webinar_btn_url": request.GET.get("closed_webinar_btn_url"),
        "fb_position": request.GET.get("fb_position"),
        "fb_title": request.GET.get("fb_title"),
        "fb_btn_text": request.GET.get("fb_btn_text"),
        "fb_btn_url": request.GET.get("fb_btn_url"),
    }

    all_aggregates = []
    category_aggregates = []
    lecturer_aggregates = []
    subcategories_pairs = []
    main_webinar = None
    related_webinars = []
    lecturer = None
    aggregates_map = {}
    cta_href = ""
    cta_text = ""
    program = ""

    # Webinar
    webinar_id = request.GET.get("webinar_id")
    if webinar_id:
        main_webinar = get_object_or_404(Webinar, pk=int(webinar_id))
        lecturer = main_webinar.lecturer
        cta_href = f"{BASE_URL}/szkl/{main_webinar.id}"  # type: ignore
        cta_href += "/{TRACKING_CODE}/{CAMPAIGN_ID}/{TEST_SUBJECT_ID}/"
        cta_text = "Zapisz się teraz!"

        if request.GET.get("use_markdown"):
            _program = markdown(main_webinar.program_markdown)
        else:
            _program = main_webinar.program

        program: str = _program

        # Related webinars
        for related_webinar in WebinarService(main_webinar).get_related_webinars():
            related_webinars.append(
                (
                    related_webinar,
                    f"{BASE_URL}/szkl/{related_webinar.id}" + "/{TRACKING_CODE}/{CAMPAIGN_ID}/",  # type: ignore
                )
            )

    # Service offer
    service_offer_id = request.GET.get("service_offer_id")
    if service_offer_id:
        service_offer = get_object_or_404(ServiceOffer, pk=int(service_offer_id))
    else:
        service_offer = None

    # (Short) Service offer
    short_service_offer_id = request.GET.get("short_service_offer_id")
    if short_service_offer_id:
        short_service_offer = get_object_or_404(
            ServiceOffer, pk=int(short_service_offer_id)
        )
    else:
        short_service_offer = None

    # Category webinars
    category_slug = request.GET.get("category_slug")

    if category_slug:
        main_category = get_object_or_404(WebinarCategory, slug=category_slug)
        subcategories = WebinarCategory.manager.get_subcategories(main_category)
        category_aggregates = (
            WebinarAggregate.manager.get_active_aggregates_for_category_slugs(
                [category_slug, *[_.slug for _ in subcategories]]
            ).filter(has_active_webinars=True)
        )
        subcategories_pairs = split_pairs(subcategories)

    # Lecturer webinars
    lecturer_slug = request.GET.get("lecturer_slug")
    if lecturer_slug:
        lecturer = Lecturer.manager.get(slug=lecturer_slug)
        lecturer_aggregates = WebinarAggregate.manager.get_active_aggregates().filter(
            Q(lecturer=lecturer) & Q(has_active_webinars=True)
        )

    for aggregate in category_aggregates:
        if aggregate not in all_aggregates:
            all_aggregates.append(aggregate)

    for aggregate in lecturer_aggregates:
        if aggregate not in all_aggregates:
            all_aggregates.append(aggregate)

    # Create keys for durations
    for aggregate in all_aggregates:

        if aggregates_map.get(aggregate.duration) is None:
            aggregates_map[aggregate.duration] = []  # type: ignore

        aggregates_map[aggregate.duration].append(aggregate)

    # Make webinar pairs
    for key, value in aggregates_map.items():
        aggregates_map[key] = split_pairs(value)

    td_classes = [
        "border-collapse:collapse;",
        "padding-left:20px;",
        "padding-right:20px;",
        "font-size: 16px;",
    ]
    shuffle(td_classes)

    return TemplateResponse(
        request,
        "mailing_templates/GlobalMailingTemplate.html",
        {
            "main_webinar": main_webinar,
            "related_webinars": related_webinars,
            "lecturer": lecturer,
            "aggregates_map": aggregates_map,
            "subcategories_pairs": subcategories_pairs,
            "BASE_URL": BASE_URL,
            "td_classes": "".join(td_classes),
            "cta_href": cta_href,
            "cta_text": cta_text,
            "program": program,
            "service_offer": service_offer,
            "short_service_offer": short_service_offer,
            **controls,
        },
    )
