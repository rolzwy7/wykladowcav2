from django.contrib.admin import ModelAdmin, register

from core.models import DiscountCode


@register(DiscountCode)
class DiscountCodeModelAdmin(ModelAdmin):
    """Model admin for `DiscountCode` model"""

    list_display = [
        "discount_code",
        "discount_value",
        "discount_type",
        "use_type",
        "expires",
        "expired",
    ]
