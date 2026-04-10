from pathlib import Path

from pathvalidate import is_valid_filename


def validate_directory_name(name: str):
    if (
        is_valid_filename(name)
        and not Path(name).suffixes
    ):
        return True
    return False
