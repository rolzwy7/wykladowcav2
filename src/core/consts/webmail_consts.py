from pathlib import Path

from django.conf import settings

BASE_DIR = settings.BASE_DIR
ASSETS_DIR: Path = BASE_DIR.parent / "core" / "assets"

WEBMAIL_GTE10: Path = ASSETS_DIR / "webmails" / "webmail_gte10.csv"

WEBMAILS: dict[str, bool] = {}

with WEBMAIL_GTE10.open("rb") as src:
    for line in src:
        WEBMAILS[str(line, "utf8").strip("\r\n")] = True
