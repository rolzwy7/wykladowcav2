from django.forms import ModelForm

from core.models import LoyaltyProgramPayout


class LoyaltyPayoutRequestForm(ModelForm):
    """Loyalty payout request form"""

    class Meta:
        model = LoyaltyProgramPayout
        fields = [
            "invoice_attachment",
            "payout_brutto",
        ]
