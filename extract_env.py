import os
import re
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def validate_directories(prepare: dict, type: str):
    type_dir = {
        'chapter': 'Подпапки для отдельной части',
        'comic': 'Подпапки для комикса'
    }
    check_set = f'Проверьте файл настроек .env, раздел "{type_dir[type]}".'
    directories: dict = {}
    for key in prepare:
        # Недопустимые в Windows символы
        if re.search(r'[:<>"\/\\\|\?\*]|\.$', prepare[key]) is not None:
            print(
                f'Значение "{prepare[key]}" содержит недопустимые символы. '
                + check_set
            )
            continue
        # Уникальность значений
        if prepare[key] in directories.values():
            print(
                f'Значение "{prepare[key]}" не уникально, будет использовано'
                + ' только первое появление. '
                + check_set
            )
            continue
        directories[key] = prepare[key]
    return directories


def directories_comic():
    """Список имен папок, в которых будут хранится ярлыки."""
    prepare = {
        'original': os.getenv('ORIGINAL_COMICS', False),
        'translate': os.getenv('TRANSLATE_COMICS', False),
        'editor': os.getenv('EDITOR_COMICS', False),
        'text': os.getenv('TEXT_COMICS', False),
    }
    directories = validate_directories(prepare, 'comic')
    return directories


def directories_chapter():
    """Список имен папок внутри части."""
    prepare = {
        'original': os.getenv('ORIGINAL_CHAPTER', 'Original'),
        'translate': os.getenv('TRANSLATE_CHAPTER', False),
        'editor': os.getenv('EDITOR_CHAPTER', False),
        'text': os.getenv('TEXT_CHAPTER', False),
    }
    directories = validate_directories(prepare, 'chapter')
    if directories.get('original') is None:
        directories['original'] = 'Original'
    return directories


def base_dir():
    base_dir = Path(os.getenv('BASE_DIR', ''))
    if (
        base_dir.is_absolute()
        and base_dir.is_dir()
    ):
        return base_dir
    print(
        'Путь BASE_DIR указан неверно. Возможные причины:'
        '\n- путь не абсолютен,'
        '\n- путь не существует,'
        '\n- путь не ведет к папке.'
    )
    return False


def length_number():
    length_number = os.getenv('LENGTH_NUMBER', '2')
    if (
        length_number.isdecimal()
        and len(length_number) < 10
    ):
        return int(length_number)
    print(
        'Число LENGTH_NUMBER указано неверно. Возможные причины:'
        '\n- число слишком большое (не больше десяти символов),'
        '\n- число содержит не только цифры.'
        "\nВ качестве LENGTH_NUMBER будет использовано число '2'."
    )
    return 2


BASE_DIR = base_dir()

LENGTH_NUMBER = length_number()
