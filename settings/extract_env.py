from os import getenv
from pathlib import Path

from pathvalidate import is_valid_filepath

from .validators import validate_directory_name


def base_dir():
    """
    Извлечение и валидация пути, указанного в качестве главной папки.

    Требования: путь правильной оформлен, путь абсолютен
    и якорь пути существует.
    """
    path = Path(getenv('BASE_DIR'))
    if (
        is_valid_filepath(path, 'auto')
        and path.is_absolute()
        and Path(path.anchor).exists()
    ):
        return path
    else:
        return False


def universal_directory(key: str, default: str):
    """
    Извлечение имён именованных директорий.

    Возвращает полученное из .env значение, если оно подходит для имени папки,
    иначе возвращает значение переменной default.
    """
    name_directory = getenv(key, '').strip()
    if validate_directory_name(name_directory):
        return name_directory
    return default


def additional_directories(*args_named_dirs):
    """
    Извлечение имён для дополнительных директорий.

    Функция вернёт прошедшие валидацию уникальные элементы,
    которых нет в предоставленной последовательности (в *args_named_dirs).
    """
    directories = {
        string.strip()
        for string
        in getenv('ADDITIONAL_FOLDERS', '').split(',')
        if (
            string.strip() not in args_named_dirs
            and validate_directory_name(string)
        )
    }
    return tuple(directories)


def length_number(min_length: int, max_length: int):
    """Извлечение длины числа для начальной нумерации имен глав комикса."""
    length_number = getenv('LENGTH_NUMBER', str(min_length))
    if length_number.isdecimal():
        number = int(length_number)
        if max_length >= number >= min_length:
            return number
        elif number > max_length:
            return max_length
        elif min_length > number:
            return min_length
    return min_length


def delete_file():
    value = getenv('DELETE')
    delete = True if value == 'True' else False
    return delete
