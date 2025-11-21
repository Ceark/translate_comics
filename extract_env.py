from os import getenv
from re import search
from pathlib import Path

from dotenv import load_dotenv


def validate_name_directory(word: str):
    """
    Валидация имени папки для Windows.
    Если полученная строка содержит недопустимые символы, вернет False.
    """
    if not search(r'[:<>"\/\\\|\?\*]|\.$', word):
        return True
    return False


def universal_directory(key: str, default: str):
    """
    Функция извлекает из .env файла значение 'key' и, если оно проходит
    валидацию, возвращает его, в противном случае возвращает 'default'.
    """
    name_directory = getenv(f'{key}', '').strip()
    if validate_name_directory(name_directory):
        return name_directory
    return default


def additional_directories():
    named_dir = (ORIGINAL, EDITOR, TRANSLATE)
    directories = {
        string.strip() for string
        in getenv('ADDITIONAL_FOLDERS', '').split(',')
        if (
            string not in named_dir
            and validate_name_directory(string)
        )
    }
    return list(directories)


def validate_base_dir():
    """
    Валидация пути, указанного в качестве главной папки.

    Если путь не абсолютен, не ведет к папке, вернет False.
    """
    path = Path(getenv('BASE_DIR', ''))
    if (
        path.is_absolute()
        and path.is_dir()
    ):
        return path
    print(
        'Путь BASE_DIR указан неверно. Возможные причины:',
        r'- путь не абсолютен (пример: D:\Папка\Папка),',
        '- путь не существует,',
        '- путь не ведет к папке.',
        sep='\n'
    )
    return False


def length_number():
    length_number = getenv('LENGTH_NUMBER', '2')
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
    value = getenv('DELETE', '')
    if value.isdecimal():
        return bool(int(value))
    return False


path_env = Path('.', '.env')
if not load_dotenv(path_env):
    with open('.env', 'w', encoding='utf-8') as file:
        base = input('Абсолютный путь к папке для BASE_DIR:\n')
        text_file = '\n\n'.join(
            [
                f'BASE_DIR = {base}',
                'ORIGINAL = Original',
                'EDITOR = Editor',
                'TRANSLATE = Translate',
                'ADDITIONAL_FOLDERS = Text',
                'LENGTH_NUMBER = 2',
                'DELETE = 0'
            ]
        )
        file.write(text_file)
    print('Файл настроек создан. Вы можете изменить их через Блокнот.')
    load_dotenv(path_env)

BASE_DIR = validate_base_dir()

ORIGINAL = universal_directory('ORIGINAL', 'Original')

EDITOR = universal_directory('EDITOR', 'Editor')

TRANSLATE = universal_directory('TRANSLATE', 'Translate')

ADDITIONAL = additional_directories()

LENGTH_NUMBER = length_number()

DELETE = delete_file()
