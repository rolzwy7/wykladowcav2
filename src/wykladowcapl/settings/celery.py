from .base_profile import APP_ENV
from .redis import REDIS_DB, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_USER

CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True
CELERY_TIMEZONE = "Europe/Warsaw"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Celery 5.* depracation warning before Celery 6.* release
# CPendingDeprecationWarning: The broker_connection_retry configuration
# setting will no longer determine whether broker connection retries are
# made during startup in Celery 6.0 and above. If you wish to retain the
# existing behavior for retrying connections on startup, you should set
# `broker_connection_retry_on_startup` to True.
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

if APP_ENV == "develop":
    CELERY_BROKER_URL = "redis://redis:6379/5"
else:
    user_pass = f"{REDIS_USER}:{REDIS_PASSWORD}"
    host_port = f"{REDIS_HOST}:{REDIS_PORT}"
    CELERY_BROKER_URL = f"redis://{user_pass}@{host_port}/{REDIS_DB}"
