import json
from pathlib import Path

default_settings = {
    'base_dir': Path().cwd(),
    'original': 'Original',
    'editor': 'Редактор',
    'translate': 'Перевод',
    'other_folder': ['Текст'],
    'delete': False,
    'length_number': 2
}


def custom_load_json(dct):
    if Path(dct['base_dir']).exists():
        dct['base_dir'] = Path(dct['base_dir'])
    else:
        dct['base_dir'] = Path().cwd()
    return dct


def download_settings(path: Path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            settings = json.load(file, object_hook=custom_load_json)
            return settings
    except (FileNotFoundError,):
        return default_settings
