from .base_profile import APP_ENV

if APP_ENV == "develop":
    FAKTUROWNIA_API_URL = "https://rolzwy7.fakturownia.pl"
    FAKTUROWNIA_API_KEY = "FI6fTUUD8Pfjg7nFwG1M"
elif APP_ENV == "production":
    ...
elif APP_ENV == "staging":
    FAKTUROWNIA_API_URL = "https://rolzwy7.fakturownia.pl"
    FAKTUROWNIA_API_KEY = "FI6fTUUD8Pfjg7nFwG1M"
elif APP_ENV == "testing":
    ...
