import os
import shutil
from pathlib import Path

import bs4
import pyinputplus as pyip
from dotenv import load_dotenv

load_dotenv()

CANCEL = 'Действие отменено.'


def create_comics():
    directories = [
        os.getenv('ORIGINAL_COMICS', False),
        os.getenv('TRANSLATE_COMICS', False)
    ]
    blockRegexes = [
        ('|'.join(os.listdir()), 'Папка с таким названием уже существует.'),
        (r'\.$', 'Точка не может стоять в конце.'),
        (r'[:<>”\/\\\|\?\*]', 'Использованы недопустимые символы.')
    ]
    name_new_comic = pyip.inputStr(
        prompt='Название нового комикса: ',
        blockRegexes=blockRegexes,
        blank=True
    )
    if not name_new_comic:
        return CANCEL
    for directory in directories:
        if directory:
            os.makedirs(Path(name_new_comic, directory))
    return f'Создана папка для комикса "{name_new_comic}".'


def choose_comics():
    list_comics = [value for value in os.listdir() if Path(value).is_dir()]
    if not list_comics:
        return ''
    choose_comics = pyip.inputMenu(
        list_comics,
        numbered=True,
        prompt='Выберете комикc:\n',
        blank=True
    )
    return choose_comics


def create_new_chapter():
    LONG_NUMBER = os.getenv('LONG_NUMBER', '2')
    LONG_NUMBER = int(LONG_NUMBER) if LONG_NUMBER.isdecimal() else 2
    directories = [
        os.getenv('ORIGINAL', False),
        os.getenv('TRANSLATE', False),
        os.getenv('EDITOR', False),
        os.getenv('TEXT', False),
    ]
    comics = choose_comics()
    if not comics:
        return CANCEL
    repeat = pyip.inputInt(
        prompt='Сколько частей создать?\n',
        blank=True,
        min=1
    )
    if not repeat:
        return CANCEL
    chapters = [
        chapter for chapter in os.listdir(comics) if chapter not in directories
    ]
    number = max(chapters) if chapters else '0'
    if not number.isdecimal():
        number = number.split('_')[0]
        if not number.isdecimal():
            number = len(chapters)
    number = int(number) + 1
    for number_chapter in range(number, number + repeat):
        long_number = str(number_chapter).rjust(LONG_NUMBER, '0')
        for directory in directories:
            if directory:
                os.makedirs(Path(comics, long_number, directory))
    if int(repeat) == 1:
        return 'Новая часть и подпапки созданы.'
    else:
        return f'Новые части ({repeat}) и подпапки созданы.'


# def extract_image():
    # comics = choose_comics()
    # for chapter in os.listdir(comics):
        # path_chapter_original = Path(os.getcwd(), comics, chapter, ORIGINAL)
        # if not path_chapter_original.exists():
            # continue
        # flag_htm = False
        # for value in os.listdir(path_chapter_original):
            # path = Path(path_chapter_original, value)
            # if path.is_dir():
                # site_dir = path
            # elif path.is_file():
                # site_file = path
                # if '.htm' in str(path):
                    # flag_htm = True
        # if not flag_htm:
            # continue
        # example_file = open(site_file, "r", encoding="utf-8")
        # example_soup = bs4.BeautifulSoup(example_file.read(), 'html.parser')
        # elems = example_soup.select('article > img')
        # file_names = [value.get('data-src').split('/')[5].split('?')[0] for value in elems]
        # for index, file in enumerate(file_names):
            # format_file = file.split('.')[-1]
            # shutil.move(
                # site_dir / file,
                # path_chapter_original / f'{index + 1}.{format_file}'
            # )


def extract_image():
    """
    Извлечь изображения из папки с файлами скачанной страницы.
    
    Предполагается, что в папке ORIGINAL будут одна папка, с
    материалами к странице, и один .htm файл, файл страницы.
    """
    comics = choose_comics()
    original = os.getenv('ORIGINAL', '')
    for chapter in os.listdir(comics):
        path_chapter_original = Path(comics, chapter, original)
        if not path_chapter_original.exists():
            continue
        flag_htm = False
        for value in os.listdir(path_chapter_original):
            path = Path(path_chapter_original, value)
            if path.is_dir():
                site_dir = path
            elif path.is_file():
                site_file = path
                flag_htm = True if '.htm' in str(path) else False
        if not flag_htm:
            continue
        example_file = open(site_file, "r", encoding="utf-8")
        example_soup = bs4.BeautifulSoup(example_file.read(), 'html.parser')
        elems = example_soup.select('article > img')
        file_names = [value.get('data-src').split('/')[5].split('?')[0] for value in elems]
        for index, file in enumerate(file_names):
            format_file = file.split('.')[-1]
            shutil.move(
                site_dir / file,
                path_chapter_original / f'{index + 1}.{format_file}'
            )
