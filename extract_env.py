import os

from dotenv import load_dotenv

load_dotenv()


def directories_comic():
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
        'original': os.getenv('ORIGINAL', False),
        'translate': os.getenv('TRANSLATE', False),
        'editor': os.getenv('EDITOR', False),
        'text': os.getenv('TEXT', False),
    }
    directories = {
        key: directories[key]
        for key in directories
        if directories[key]
    }
    return directories
