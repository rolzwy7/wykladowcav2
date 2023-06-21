from dataclasses import dataclass


@dataclass
class VatExemption:
    db_key: str  # Key that will be save in database
    description: str
    identifier: int  # For 3rd party invoiving API
    legal_basis: str
