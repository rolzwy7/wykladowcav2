# flake8: noqa: E501
# pylint: disable=line-too-long

from dataclasses import dataclass

from core.models.enums import WebinarApplicationType


@dataclass
class VatExemption:
    db_key: str  # Key that will be save in database
    description: str
    identifier: int  # For 3rd party invoiving API
    legal_basis: str


VAT_EXEMPTION_0 = VatExemption("VAT_EXEMPTION_0", "Brak zwolnienia z VAT", 0, "")

VAT_EXEMPTION_13 = VatExemption(
    "VAT_EXEMPTION_13",
    "art. 43. ust. 1 pkt 29 lit. c - Szkolenia zawodowe finansowane ze środków publicznych",
    13,
    "art. 43. ust. 1 pkt 29 lit. c",
)

VAT_EXEMPTION_36 = VatExemption(
    "VAT_EXEMPTION_36",
    "par. 3. ust. 1 pkt 14 - Szkolenia zawodowe dofinansowane co najmniej w 70% ze środków publicznych",  # noqa
    36,
    "par. 3. ust. 1 pkt 14",
)

VAT_EXEMPTION_113 = VatExemption(
    "VAT_EXEMPTION_113",
    "Faktura wystawiana bez podatku VAT na podstawie art. 113 ust. 1 i 9 ustawy o VAT",  # noqa
    36,
    "art. 113 ust. 1 i 9 ustawy o VAT",
)

# True if we are exempt from income TAX up to 200,000 PLN
# What does it do?:
# - Hides select input on application form page
WE_ARE_TAX_EXEMPT = False

# VAT percent value
VAT_VALUE_PERCENT = 23

# Tooltip with text explaining why we are tax exempt
TAX_EXEMPT_TOOLTIP = VAT_EXEMPTION_113.description

# Visible next to price: "350zł {{PRICE_ADNOTATION}}"
if WE_ARE_TAX_EXEMPT:
    PRICE_ADNOTATION = "netto/brutto"
else:
    PRICE_ADNOTATION = f"+ {VAT_VALUE_PERCENT}% VAT"

# Here place ALL defined VAT exemptions
VAT_EXEMPTIONS = [
    VAT_EXEMPTION_0,
    VAT_EXEMPTION_13,
    VAT_EXEMPTION_36,
    VAT_EXEMPTION_113,
]


def to_choices(exemptions_list: list[VatExemption]):
    """Convert list of exemptions to select choices"""
    return [(exemption.db_key, exemption.description) for exemption in exemptions_list]


# Choices for `CharField.choices` argument
CHOICES_VAT_EXEMPTIONS = to_choices(VAT_EXEMPTIONS)

# Here define which types of applications can be exempt from VAT
if WE_ARE_TAX_EXEMPT:
    ALLOWED_EXEMPTIONS_BY_APPLICATION_TYPE = {
        WebinarApplicationType.COMPANY: to_choices([VAT_EXEMPTION_113]),
        WebinarApplicationType.JSFP: to_choices([VAT_EXEMPTION_113]),
        WebinarApplicationType.PRIVATE_PERSON: to_choices([VAT_EXEMPTION_113]),
    }
else:
    ALLOWED_EXEMPTIONS_BY_APPLICATION_TYPE = {
        WebinarApplicationType.COMPANY: to_choices([VAT_EXEMPTION_0, VAT_EXEMPTION_13]),
        WebinarApplicationType.JSFP: to_choices(
            [
                VAT_EXEMPTION_0,
                VAT_EXEMPTION_13,
                VAT_EXEMPTION_36,
            ]
        ),
        WebinarApplicationType.PRIVATE_PERSON: to_choices([VAT_EXEMPTION_0]),
    }
