from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.timezone import now, timedelta

from core.consts import POST
from core.models import DiscountCode, WebinarApplicationCancellation
from core.models.enums import DiscountCodeType, DiscountCodeUseType
from core.services.discount_service import DiscountService


def webinar_cancellation_page(request: HttpRequest, token: str):
    """Webinar cancellation page controller"""
    template_name = (
        "core/pages/crm/webinar_cancellation/WebinarCancellationPage.html"
    )
    webinar_cancellation = get_object_or_404(
        WebinarApplicationCancellation, token=token
    )

    # Note the link click
    if webinar_cancellation.clicked_in_link is False:
        webinar_cancellation.clicked_in_link = True
        webinar_cancellation.save()

    # If cancellation is already confirmed then just return template
    if webinar_cancellation.confirmed:
        return TemplateResponse(
            request,
            template_name,
            {"webinar_cancellation": webinar_cancellation},
        )

    # On form submit
    if request.method == POST:
        # Create new discount code
        discount_code = DiscountService.generate_unused_discount_code()
        DiscountCode(
            discount_code=discount_code,
            discount_value=10,
            use_type=DiscountCodeUseType.ONE_TIME,
            discount_type=DiscountCodeType.PERCENT,
            expires=now() + timedelta(days=14),
        ).save()

        # Save disocunt code in `webinar_cancellation`
        webinar_cancellation.discount_code = discount_code

        # Mark `webinar_cancellation` as confirmed
        webinar_cancellation.confirmed = True

        # Save
        webinar_cancellation.save()

    return TemplateResponse(
        request, template_name, {"webinar_cancellation": webinar_cancellation}
    )
