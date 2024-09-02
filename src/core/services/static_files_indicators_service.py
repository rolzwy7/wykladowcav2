"""Static Files Indicator Service"""

# flake8: noqa=E501

from pathlib import Path

from django.conf import settings

BASE_DIR = settings.BASE_DIR
ASSETS_DIR: Path = BASE_DIR.parent / "public" / "static"


class StaticFilesIndicatorsService:

    def __init__(self) -> None:
        pass

    def get_disc_space_context(self):
        """Get disc space"""
        filepath = ASSETS_DIR / "disc_space.txt"

        if filepath.exists() and filepath.is_file():
            try:
                date, taken, no_recordings = filepath.open("r").readlines()
            except Exception as e:
                date, taken, no_recordings = "error", "error", "error"
        else:
            date, taken, no_recordings = "no_file", "no_file", "no_file"

        date = date.strip()
        taken = taken.strip()
        no_recordings = no_recordings.strip()

        try:
            taken_num = float(taken)
            progress_bar_width = int(100 * taken_num / 200.0)
            if progress_bar_width > 90:
                progress_bar_color = "danger"
            elif progress_bar_width > 70:
                progress_bar_color = "warning"
            else:
                progress_bar_color = "success"

        except Exception as e:
            progress_bar_color = "secondary"
            progress_bar_width = "50"

        return {
            "date": date.strip(),
            "taken": taken.strip(),
            "no_recordings": no_recordings.strip(),
            "progress_bar_color": progress_bar_color,
            "progress_bar_width": progress_bar_width,
        }

    def get_tmux_processes_context(self):
        """Get Tmux Processes Context"""

        filepath = ASSETS_DIR / "tmux_list.txt"

        if filepath.exists() and filepath.is_file():
            try:
                lines = filepath.open("r").readlines()
                checked_at = lines[0]
                processes = lines[1:]
            except Exception as e:
                checked_at, processes = "error", ["error"]
        else:
            checked_at, processes = "no_file", ["no_file"]

        return {
            "checked_at": checked_at.strip(),
            "processes": processes,
        }
