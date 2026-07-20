import json
from pathlib import Path

from custom_typing import PythonTwoSettings

default_settings: PythonTwoSettings = {
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
    if Path(dct['base_dir']).exists():
        dct['base_dir'] = Path(dct['base_dir'])
    else:
        dct['base_dir'] = Path().cwd()
    return dct


def load_settings(path: Path) -> PythonTwoSettings:
    """
    Загрузить настройки из json-файла.

    Поле 'base_dir' обрабатывается отдельно, см. object_hook.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            settings = json.load(file, object_hook=custom_object_hook)
            return settings
    except (FileNotFoundError,):
        return default_settings


def default_for_path(obj):
    """
    Обработка объектов Path для json.
    """
    if isinstance(obj, Path):
        return f"{obj._raw_path}"
    raise TypeError(f'Cannot serialize object of {type(obj)}')


def save_dict_settings(path: Path, dct: PythonTwoSettings):
    """
    Сохранить словарь настроек как json-файл.
    """
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(
            dct, file, indent=4, ensure_ascii=False,
            default=default_for_path
        )
