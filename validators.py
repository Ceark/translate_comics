from pathlib import Path
from re import search


def validate_name_directory(word: str):
    """
    Валидация имени папки для Windows, проверяются символы.
    """
    if word and not search(r'[:<>"\/\\\|\?\*]|\.$', word):
        return True
    return False


def validate_dir(path: Path):
    if (
        path.is_absolute()
        and path.is_dir()
    ):
        return True
    return False
