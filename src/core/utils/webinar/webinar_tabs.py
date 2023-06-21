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
        ),
        (
            "Opinie",
            "core:webinar_opinions_page",
        ),
        (
            "Cena i Faktura",
            "core:webinar_price_and_invoice_page",
        ),
        (
            "O wykładowcy",
            "core:webinar_lecturer_biography_page",
        ),
    ]
    _tab_index = (
        tab_index if all([tab_index >= 0, tab_index < len(tabs)]) else 0
    )
    return [
        (
            tab_name,
            reverse(url_name, kwargs={"slug": webinar_slug}),
            idx == _tab_index,
        )
        for idx, (tab_name, url_name) in enumerate(tabs)
    ]
