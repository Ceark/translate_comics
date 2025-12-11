from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from validators import validate_name_directory, validate_dir


def universal_directory(key: str, default: str):
    """
    Извлечение имён для именованных директорий.

    Функция извлекает переменную 'key', и, если она пройдёт
    валидацию, вернёт её значение; в противном случае будет передано значение
    'default'.
    """
    name_directory = getenv(f'{key}', '').strip()
    if validate_name_directory(name_directory):
        return name_directory
    return default


def additional_directories(*args_named_dirs):
    """
    Извлечение имён для дополнительных директорий.

    Функция вернёт те элементы, которые прошли валидацию
    и которых нет в 'args_named_dirs', элементы не повторяются.
    """
    directories = {
        string.strip() for string
        in getenv('ADDITIONAL_FOLDERS', '').split(',')
        if (
            string.strip() not in args_named_dirs
            and validate_name_directory(string)
        )
    }
    return tuple(directories)


def base_dir():
    """
    Валидация пути, указанного в качестве главной папки.

    Требования: путь абсолютен, путь ведёт к существуещей папке.
    """
    path = Path(getenv('BASE_DIR', ''))
    if validate_dir(path):
        return path
    print(
        'Путь BASE_DIR указан неверно. Возможные причины:',
        r'- путь не абсолютен (пример: D:\Папка\Папка),',
        '- путь не существует,',
        '- путь не ведет к папке.',
        sep='\n'
    )
    return False


def length_number(min_length: int, max_length: int):
    """Извлечение длины числа для начальной нумерации имен папок."""
    length_number = getenv('LENGTH_NUMBER', str(min_length))
    if (
        length_number.isdecimal()
        and int(length_number) < max_length
    ):
        return int(length_number)
    print(
        'Число LENGTH_NUMBER указано неверно. Возможные причины:',
        f'- число слишком большое (максимум - {max_length});',
        '- число содержит не только цифры.',
        f'В качестве LENGTH_NUMBER будет использовано число {min_length}.',
        sep='\n'
    )
    return min_length


def delete_file():
    """
    Извлечени согласия на удаление (в корзину) файлов комикса после извлечения.

    1 (True) - удалить файлы, 0 или '' (False) - не удалять файлы.
    """
    value = getenv('DELETE', '')
    if value.isdecimal():
        return bool(int(value))
    return False


path_env = Path('.', '.env')
if not load_dotenv(path_env):
    with open('.env', 'w', encoding='utf-8') as file:
        base = input('Абсолютный путь к папке для комиксов:\n')
        text_file = '\n\n'.join(
            (
                f'BASE_DIR = {base}',
                'ORIGINAL = Original',
                'EDITOR = Editor',
                'TRANSLATE = Translate',
                'ADDITIONAL_FOLDERS = Text',
                'LENGTH_NUMBER = 2',
                'DELETE = 0'
            )
        )
        file.write(text_file)
    print(
        'Настройки можно изменить через Блокнот.',
        'Файл настроек находится рядом с файлом программы.',
        '-----'
    )
    load_dotenv(path_env)

BASE_DIR = base_dir()

ORIGINAL = universal_directory('ORIGINAL', 'Original')

EDITOR = universal_directory('EDITOR', 'Editor')

TRANSLATE = universal_directory('TRANSLATE', 'Translate')

NAMED_DIRS = (ORIGINAL, EDITOR, TRANSLATE)

ADDITIONAL = additional_directories(NAMED_DIRS)

LENGTH_NUMBER = length_number(2, 4)

DELETE = delete_file()
