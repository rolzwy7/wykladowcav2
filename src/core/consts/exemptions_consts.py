from dataclasses import dataclass

from core.models.enums import WebinarApplicationType


@dataclass
class VatExemption:
    db_key: str  # Key that will be save in database
    description: str
    identifier: int  # For 3rd party invoiving API
    legal_basis: str


VAT_EXEMPTION_0 = VatExemption(
    "VAT_EXEMPTION_0", "Brak zwolnienia z VAT", 0, ""
)

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

# True if we are exempt from income TAX up to 200,000 PLN
# What does it do?:
# - Hides select input on application form page
WE_ARE_TAX_EXEMPT = True

# Here place ALL defined VAT exemptions
VAT_EXEMPTIONS = [
    VAT_EXEMPTION_0,
    VAT_EXEMPTION_13,
    VAT_EXEMPTION_36,
]

# Choices for `CharField.choices` argument
CHOICES_VAT_EXEMPTIONS = [
    (exemption.db_key, exemption.description) for exemption in VAT_EXEMPTIONS
]

# Here define which types of applications can be exempt from VAT
ALLOWED_EXEMPTIONS_BY_APPLICATION_TYPE = {
    WebinarApplicationType.COMPANY: [VAT_EXEMPTION_0, VAT_EXEMPTION_13],
    WebinarApplicationType.JSFP: [
        VAT_EXEMPTION_0,
        VAT_EXEMPTION_13,
        VAT_EXEMPTION_36,
    ],
    WebinarApplicationType.PRIVATE_PERSON: [VAT_EXEMPTION_0],
}
