from django.urls import reverse


def get_webinar_tabs(tab_index: int, webinar_slug: str):
    """Returns structure for generating webinar tabs

    Args:
        tab_index (int): tab to be active
        webinar_slug (str): webinar url slug

    Returns:
        _type_: _description_
    """
    tabs = [
        (
            "Program szkolenia",
            "core:webinar_program_page",
            "ki-book-open",
        ),
        (
            "Opinie",
            "core:webinar_opinions_page",
            "ki-like-shapes",
        ),
        (
            "Cena i Faktura",
            "core:webinar_price_and_invoice_page",
            "ki-price-tag",
        ),
        (
            "O wykładowcy",
            "core:webinar_lecturer_biography_page",
            "ki-teacher",
        ),
    ]
    _tab_index = (
        tab_index if all([tab_index >= 0, tab_index < len(tabs)]) else 0
    )
    return [
        (
            title,  # tab title
            reverse(url_name, kwargs={"slug": webinar_slug}),  # url
            idx == _tab_index,  # is active
            icon,  # icon
        )
        for idx, (title, url_name, icon) in enumerate(tabs)
    ]
