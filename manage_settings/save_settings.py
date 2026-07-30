import json
from pathlib import Path

from custom_typing.custom_typing import Settings


def default_for_path(obj):
    """
    Обработка объектов Path для json.
    """
    if isinstance(obj, Path):
        return f"{obj._raw_path}"
    raise TypeError(f'Cannot serialize object of {type(obj)}')


def save_dict_settings(path: Path, dct: Settings):
    """
    Сохранить словарь настроек как json-файл.
    """
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(
            dct, file, indent=4, ensure_ascii=False,
            default=default_for_path
        )
