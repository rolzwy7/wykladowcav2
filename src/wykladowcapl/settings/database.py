from .base_profile import APP_ENV, BASE_DIR

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if APP_ENV == "production":
    ...
elif APP_ENV == "staging":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "OPTIONS": {
                "service": "postgres_db_service",
                "passfile": ".pgpass",
            },
        }
    }
elif APP_ENV == "develop":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
