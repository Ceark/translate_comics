import os
import shutil
from pathlib import Path

import bs4
import pyinputplus as pyip
from dotenv import load_dotenv

from extract_env import directories_chapter, directories_comic

load_dotenv()

CANCEL = 'Действие отменено.'


def create_comic():
    directories = directories_comic()
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
    for directory in directories.values():
        os.makedirs(Path(name_new_comic, directory))
    return f'Создана папка для комикса "{name_new_comic}".'


def choose_comic():
    list_comics = [value for value in os.listdir() if Path(value).is_dir()]
    if not list_comics:
        return ''
    choose_comic = pyip.inputMenu(
        list_comics,
        numbered=True,
        prompt='Выберете комикc:\n',
        blank=True
    )
    return choose_comic


def list_chapters(comic, directories):
    chapters = [
        chapter for chapter in os.listdir(comic) if (
            chapter not in directories.values()
            and Path(comic, chapter).is_dir()
        )
    ]
    return chapters


def create_new_chapter():
    LONG_NUMBER = os.getenv('LONG_NUMBER', '2')
    LONG_NUMBER = int(LONG_NUMBER) if LONG_NUMBER.isdecimal() else 2
    directories = directories_chapter()
    comic = choose_comic()
    if not comic:
        return CANCEL
    repeat = pyip.inputInt(
        prompt='Сколько частей создать?\n',
        blank=True,
        min=1
    )
    if not repeat:
        return CANCEL
    chapters = list_chapters(comic, directories)
    number = max(chapters) if chapters else '0'
    if not number.isdecimal():
        number = number.split('_')[0]
        if not number.isdecimal():
            number = len(chapters)
    number = int(number) + 1
    for number_chapter in range(number, number + repeat):
        long_number = str(number_chapter).rjust(LONG_NUMBER, '0')
        for directory in directories.values():
            os.makedirs(Path(comic, long_number, directory))
    if int(repeat) == 1:
        return 'Новая часть и подпапки созданы.'
    else:
        return f'Новые части ({repeat}) и подпапки созданы.'


def extract_image():
    comic = choose_comic()
    if not comic:
        return CANCEL
    directories = directories_comic()
    chapters = list_chapters(comic, directories)
    for chapter in chapters:
        path = Path(comic, chapter, directories['original'])
        if not path.exists():
            continue
        flag = [False, False]
        for value in os.listdir(path):
            if Path(path, value).is_dir():
                path_site_dir = Path(path, value)
                flag[0] = True
            elif Path(path, value).is_file():
                path_site_file = Path(path, value)
                flag[0] = True
        if not (flag[0] and flag[1]):
            continue
        example_file = open(path_site_file, "r", encoding="utf-8")
        example_soup = bs4.BeautifulSoup(example_file.read(), 'html.parser')
        elems = example_soup.select('article > img')
        file_names = [value.get('data-src').split('/')[5].split('?')[0]
                      for value in elems]
        for index, file in enumerate(file_names):
            format_file = file.split('.')[-1]
            shutil.move(
                    path_site_dir / file,
                    path / f'{index + 1}.{format_file}'
                )
        del (path_site_dir, path_site_file)
