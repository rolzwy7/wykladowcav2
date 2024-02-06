# flake8: noqa=E501
# pylint: disable=line-too-long

import os

from django.core.checks import Error, register
from dotenv import load_dotenv

load_dotenv(override=True)

MANDATORY_ENV_CONSTANTS = [
    "SECRET_KEY",
    "APP_ENV",
    "SECURE_SSL_REDIRECT",
    "ALLOWED_HOSTS",
    "SITE_DOMAIN",
    "INGKSIEGOWOSC_API_KEY",
    "CLICKMEETING_API_KEY",
    "REGON_API_KEY",
    "FAKTUROWNIA_API_URL",
    "FAKTUROWNIA_API_KEY",
    "REDIS_DB",
    "REDIS_USER",
    "REDIS_PASSWORD",
    "REDIS_HOST",
    "REDIS_PORT",
    "EMAIL_HOST",
    "EMAIL_PORT",
    "EMAIL_HOST_USER",
    "EMAIL_HOST_PASSWORD",
    "TELEGRAM_API_KEY",
    "MONGO_HOST",
    "MONGO_PORT",
    "MONGO_DB_NAME",
    "MONGO_USER",
    "MONGO_PASSWORD",
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
]


@register()
def check_env_constants(app_configs, **kwargs):
    """Check if mandatory .env constants are set"""
    errors = []

    for constant_name in MANDATORY_ENV_CONSTANTS:
        if os.environ.get(constant_name) is None:
            errors.append(
                Error(
                    "an error",
                    hint=f"System variable `{constant_name}` is missing in .env file",
                    obj=constant_name,
                    id=f"env_missing.{constant_name}",
                )
            )

    return errors
