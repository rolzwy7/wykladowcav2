from .base_profile import APP_ENV
from .redis import REDIS_DB, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_USER

CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True
CELERY_TIMEZONE = "Europe/Warsaw"

# CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 30 * 60


if APP_ENV == "develop":
    CELERY_BROKER_URL = "redis://redis:6379/5"
else:
    user_pass = f"{REDIS_USER}:{REDIS_PASSWORD}"
    host_port = f"{REDIS_HOST}:{REDIS_PORT}"
    CELERY_BROKER_URL = f"redis://{user_pass}@{host_port}/{REDIS_DB}"
