import json
from pathlib import Path

from custom.klass import Folder, update_union
from custom.typing import Settings

default_settings: Settings = {
    'base_dir': Path().cwd(),
    'original': 'Original',
    'editor': 'Редактор',
    'translate': 'Перевод',
    'other_folder': ['Текст'],
    'delete': False,
    'length_number': 2,
    'ignore_folder': ['.git'],
    'move_images': {
        'where': 'Original',
        'to': 'Редактор',
        'suffix': ''
    }
}


def custom_object_hook(dct: dict):
    """
    Замена содержимого 'base_dir' на Path-объект.

    Если указанный адрес существует, то он будет использоваться,
    иначе будет использоваться текущий адрес.
    Остальной словарь обрабатывается как обычно.
    """
    # Проверка существования 'base_dir'
    if dct.get('base_dir'):
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
    except (FileNotFoundError, Exception):
        settings = default_settings

    for key in default_settings:
        if key not in settings:
            settings[key] = default_settings[key]

    technical_folder = [
        settings['original'],
        settings['editor'],
        settings['translate']
    ] + settings['other_folder']
    update_union(Folder.technical_folders, technical_folder)
    update_union(Folder.ignored_folders, settings['ignore_folder'])
    Folder.settings = settings

    return settings
