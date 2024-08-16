# flake8: noqa:E501
# pylint: disable=line-too-long

import mimetypes
import os
import time
from pathlib import Path

from django.forms.renderers import TemplatesSetting
from dotenv import load_dotenv

load_dotenv(override=True)

VERSION_NUMBER = "1.7.0"
VERSION_DATE = "2024/08/16"

APP_START_TIMESTAMP = int(time.time())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Correct MIME types
mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/css", ".min.css", True)
mimetypes.add_type("application/javascript", ".js", True)
mimetypes.add_type("application/javascript", ".min.js", True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

APP_ENV = os.environ.get("APP_ENV", "develop")
ALLOWED_APP_ENVS = ["develop", "production", "staging", "testing"]
assert APP_ENV in ALLOWED_APP_ENVS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = APP_ENV in ["develop", "testing"]

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split("||")

AUTH_USER_MODEL = "core.User"

SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT") == "1"
HTTP_SCHEMA = "https" if SECURE_SSL_REDIRECT else "http"

SITE_DOMAIN = os.environ.get("SITE_DOMAIN", "localhost:8080")
BASE_URL = f"{HTTP_SCHEMA}://{SITE_DOMAIN}"

if DEBUG:  # Debug toolbar
    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

# Application definition

INSTALLED_APPS = [
    # Monolith apps
    "core",
    "api",
    "htmx",
    # 3rd party
    "rest_framework",
    "django_celery_results",
    "django_celery_beat",
    "tinymce",
    "debug_toolbar",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # Edit your settings.py file and add WhiteNoise to the MIDDLEWARE list
    # above all other middleware apart from Django’s SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Custom middleware
    "core.middleware.CoreMiddleware",
    "core.middleware.LoyaltyProgramMiddleware",
]

ROOT_URLCONF = "wykladowcapl.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Custom context processors
                "core.context_processors.cached",
                "core.context_processors.header",
                "core.context_processors.consts",
                "core.context_processors.crm",
                "core.context_processors.dates",
                "core.context_processors.company",
                "core.context_processors.links",
                "core.context_processors.metadata",
                # "core.context_processors.loyalty_program", # TODO: delete this ??
            ],
        },
    },
]

WSGI_APPLICATION = "wykladowcapl.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "pl-PL"

TIME_ZONE = "Europe/Warsaw"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = str((BASE_DIR.parent / "public" / "static/").absolute())

MEDIA_URL = "media/"

MEDIA_ROOT = str((BASE_DIR.parent / "public" / "media/").absolute())


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


class CustomFormRenderer(TemplatesSetting):
    """Custom form renderer class"""

    form_template_name = "core/forms/FormSnippet.html"


FORM_RENDERER = "wykladowcapl.settings.CustomFormRenderer"

# WHITENOISE_MANIFEST_STRICT = False

# STORAGES = {
#     "staticfiles": {
#         # "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#         "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
#     },
# }
