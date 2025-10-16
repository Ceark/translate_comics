import os
import re
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def validate(word):
    if not re.search(r'[:<>"\/\\\|\?\*]|\.$', word):
        return True
    return False


def original_directory():
    original = os.getenv('ORIGINAL_COMICS').strip()
    if validate(original):
        return original
    return 'Original'


def additional_directories():
    original = original_directory()
    directories = {
        string.strip() for string
        in os.getenv('ADDITIONAL_FOLDERS').split(',')
        if not string == original
    }
    return list(directories)


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
        'Число LENGTH_NUMBER указано неверно. Возможные причины:',
        '- число слишком большое (не больше десяти символов);',
        '- число содержит не только цифры.',
        'В качестве LENGTH_NUMBER будет использовано число 2.',
        sep='\n'
    )
    return 2


def delete_file():
    value = os.getenv('DELETE')
    if value.isdecimal():
        return bool(value)
    return False


BASE_DIR = base_dir()

LENGTH_NUMBER = length_number()

ORIGINAL = original_directory()

ADDITIONAL = additional_directories()

DELETE = delete_file()
