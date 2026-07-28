import json
from pathlib import Path

from custom_typing_.custom_typing import Settings

default_settings: Settings = {
    'base_dir': Path().cwd(),
    'original': 'Original',
    'editor': 'Редактор',
    'translate': 'Перевод',
    'other_folder': ['Текст'],
    'delete': False,
    'length_number': 2
}


def custom_object_hook(dct):
    """
    Замена содержимого 'base_dir' на Path-объект:
    если указанный адрес существует, то он будет использоваться, иначе
    будет использоваться текущий адрес (адрес по умолчанию).

    Остальной словарь обрабатывается как обычно.
    """
    # Проверка существования 'base_dir'
    if Path(dct['base_dir']).exists():
        dct['base_dir'] = Path(dct['base_dir'])
    else:
        dct['base_dir'] = Path().cwd()
    return dct


def load_settings(path: Path) -> Settings:
    """
    Загрузить настройки из json-файла.

    Поле 'base_dir' обрабатывается отдельно, см. object_hook.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            settings: Settings = json.load(
                file, object_hook=custom_object_hook
            )
            return settings
    except (FileNotFoundError, Exception):
        return default_settings
