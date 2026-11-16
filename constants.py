from pathlib import Path
from re import compile

path_settings = Path('settings.json')
path_site_and_selectors = Path('site_and_selectors')

strings: list[str] = [
    'Комиксы',
    'Оригинал',
    'Редактор',
    'Перевод',
    'Доп. папки',
    'Игнорировать',
    'Удалить файлы',
    'Длина числа',
    'Откуда',
    'Куда',
    'Суффикс'
]

pattern = compile(r'^\d+(?:\.\d+)?')
