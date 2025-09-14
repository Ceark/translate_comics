import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.getenv('BASE_DIR')

LENGTH_NUMBER = os.getenv('LENGTH_NUMBER', '2')


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
