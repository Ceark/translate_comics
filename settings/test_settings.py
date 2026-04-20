import tkinter as tk
from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from pathvalidate import is_valid_filepath, sanitize_filename

from .validators import validate_directory_name


class Settings:
    """
    Это класс настроек для проекта translate_comics.

    Содержит путь к папке проекта (BASE_DIR), именованные папки (ORIGINAL,
    EDITOR, TRANSLATE), дополнительные папки (ADDITIONAL_FOLDERS),
    количество знаков в главе комикса (LENGTH_NUMBER),
    согласие на удаление (DELETE).
    """
    def __init__(self):
        load_dotenv()
        names = (
            'ORIGINAL',
            'EDITOR',
            'TRANSLATE'
        )
        self.base_dir = Path(getenv('BASE_DIR', ''))
        self.named_dirs = {
            name: getenv(name, '')
            for name
            in names
            # if validate_directory_name(getenv(name, ''))
        }
        self.additional_dirs = [
            string.strip()
            for string
            in getenv('ADDITIONAL_FOLDERS', '').split(',')
            # if
        ]
        self.length_number = int(getenv('LENGTH_NUMBER', ''))
        self.delete = True if getenv('DELETE') == 'True' else False

    def update_settings(self):
        settings = {
            'base_dir': Path,
            'named_dirs': {str: str},
            'additional_dirs': [str],
            'length_number': int,
            'delete': bool
        }
        
        with open('.env', 'w', encoding='utf-8') as file:
            text_file = '\n\n'.join(
                (
                    f'BASE_DIR = {settings["base_dir"]}',
                    f'ORIGINAL = {settings}',
                    f'EDITOR = {settings}',
                    f'TRANSLATE = {settings}',
                    f'ADDITIONAL_FOLDERS = {settings}',
                    f'LENGTH_NUMBER = 2',
                    f'DELETE = 0'
                )
            )

