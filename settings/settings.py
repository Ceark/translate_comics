from os import environ
from pathlib import Path

from .extract_env import (additional_directories, base_dir, delete_file,
                          length_number, universal_directory)


def first_start(path_main_folder: Path):
    with open('.env', 'w', encoding='utf-8') as file:
        text_file = '\n\n'.join(
            (
                f'BASE_DIR = {path_main_folder}',
                'ORIGINAL = Original',
                'EDITOR = Editor',
                'TRANSLATE = Translate',
                'ADDITIONAL_FOLDERS = Text',
                'LENGTH_NUMBER = 2',
                'DELETE = False'
            )
        )
        file.write(text_file)


def update_settings(**kwargs):
    """
    Ожидаемый словарь содержит поля Base_Dir, Original, Editor, Translate,
    Additional_Folders, Length_Number, Delete.
    """
    with open('.env', 'w', encoding='utf-8') as file:
        text_file = '\n\n'.join(
            (
                f'BASE_DIR = {kwargs.get("base_dir")}',
                f'ORIGINAL = {kwargs.get("original")}',
                f'EDITOR = {kwargs.get("editor")}',
                f'TRANSLATE = {kwargs.get("translate")}',
                f'ADDITIONAL_FOLDERS = {kwargs.get("additional_folders")}',
                f'LENGTH_NUMBER = {kwargs.get("length_number")}',
                f'DELETE = {kwargs.get("delete")}'
            )
        )
        file.write(text_file)
    for value in kwargs:
        environ[value] = kwargs[value]


BASE_DIR = base_dir()

ORIGINAL = universal_directory('ORIGINAL', 'Original')

EDITOR = universal_directory('EDITOR', 'Editor')

TRANSLATE = universal_directory('TRANSLATE', 'Translate')

NAMED_DIRS = (ORIGINAL, EDITOR, TRANSLATE)

ADDITIONAL = additional_directories(NAMED_DIRS)

LENGTH_NUMBER = length_number(1, 5)

DELETE = delete_file()
