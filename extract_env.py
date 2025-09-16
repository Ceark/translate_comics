import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def directories_comic():
    """Список имен папок, в которых будут хранится ярлыки."""
    directories = {
        'original': os.getenv('ORIGINAL_COMICS', False),
        'translate': os.getenv('TRANSLATE_COMICS', False),
        'editor': os.getenv('EDITOR_COMICS', False),
        'text': os.getenv('TEXT_COMICS', False),
    }
    directories = {
        key: directories[key]
        for key in directories
        if directories[key]
    }
    return directories


def directories_chapter():
    directories = {
        'original': os.getenv('ORIGINAL_CHAPTER', 'Original'),
        'translate': os.getenv('TRANSLATE_CHAPTER', False),
        'editor': os.getenv('EDITOR_CHAPTER', False),
        'text': os.getenv('TEXT_CHAPTER', False),
    }
    directories = {
        key: directories[key]
        for key in directories
        if directories[key]
    }
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
