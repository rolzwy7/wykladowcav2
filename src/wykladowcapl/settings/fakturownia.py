from .base_profile import DEBUG

if DEBUG:
    FAKTUROWNIA_API_URL = "https://rolzwy7.fakturownia.pl"
    FAKTUROWNIA_API_KEY = "FI6fTUUD8Pfjg7nFwG1M"
else:
    ...  # TODO: Set Fakturownia's settings
