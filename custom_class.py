import os
import shutil
from pathlib import Path

import bs4
import pyinputplus as pyip

from extract_env import DIR_CHAPTER, DIR_COMIC, LENGTH_NUMBER

CANCEL = 'Действие отменено.'


class Comic:
    dir_comic = DIR_COMIC
    dir_chapter = DIR_CHAPTER
    length_number = LENGTH_NUMBER

    def __init__(self, path: Path):
        self.path = path

    def self_create(self):
        """Создание папки комикса."""
        if not self.path.exists():
            os.mkdir(self.path)
            for directory in self.dir_comic.values():
                os.mkdir(self.path / directory)
        else:
            print('Папка уже существует.')

    def list_chapters(self):
        """
        Получить список папок комикса. Файлы и папки для ярлыков исключены.
        """
        chapters = [
            chapter for chapter in os.listdir(self.path)
            if (
                chapter not in self.dir_chapter.values()
                and (self.path / chapter).is_dir()
            )
        ]
        return chapters

    def add_chapter(self, repeat):
        """
        Добавить часть.
        Номер добавленной папки определяется сначала по значению 'max'.
        Сначала пытается найти число, если не удастся, то использует
        количество папок.
        """
        chapters = self.list_chapters()
        number = max(chapters) if chapters else '0'
        if not number.isdecimal():
            number = number.split('_')[0]
            if not number.isdecimal():
                number = len(chapters)
        number = int(number) + 1
        for number_chapter in range(number, number + repeat):
            long_number = str(number_chapter).rjust(self.length_number, '0')
            for directory in self.dir_chapter.values():
                os.makedirs(self.path / long_number / directory)

    def extract_image(self):
        chapters = self.list_chapters()
        for chapter in chapters:
            # Поиск файла сайта и папки с содержимым
            path = self.path / chapter / self.dir_chapter['original']
            if not path.exists():
                continue
            path_site_dir, path_site_file = False, False
            for value in os.listdir(path):
                if Path(path, value).is_dir():
                    path_site_dir = Path(path, value)
                elif Path(path, value).is_file():
                    path_site_file = Path(path, value)
            if not (path_site_dir and path_site_file):
                continue
            # Экстракция изображений
            example_file = open(path_site_file, "r", encoding="utf-8")
            example_soup = bs4.BeautifulSoup(
                example_file.read(),
                'html.parser'
            )
            elems = example_soup.select(
                'article > img[class="content__img js-lazy"]'
            )
            file_names = [value.attrs['src'].split('/')[-1] for value in elems]
            for index, file in enumerate(file_names):
                format_file = file.split('.')[-1]
                shutil.move(
                    path_site_dir / file,
                    path / f'{index + 1}.{format_file}'
                )


class MainFolder:
    def __init__(self, path: Path):
        self.path = path

    def create_comic(self):
        blockRegexes = [
            (
                '|'.join(os.listdir(self.path)),
                'Папка с таким названием уже существует.'
            ),
            (
                r'\.$',
                'Точка не может стоять в конце названия папки.'
            ),
            (
                r'[:<>"\/\\\|\?\*]',
                'В названии папки использованы недопустимые символы.'
            )
        ]
        name_new_comic = pyip.inputStr(
            prompt='Название нового комикса: ',
            blockRegexes=blockRegexes,
            blank=True
        )
        if not name_new_comic:
            return 'Действие отменено.'
        comic = Comic(path=self.path / name_new_comic)
        comic.self_create()
        return f'Создана папка для комикса "{name_new_comic}".'

    def choose_comic(self):
        list_comics = [
            value for value in os.listdir(self.path)
            if (self.path / value).is_dir()
        ]
        if list_comics:
            choose_comic = pyip.inputMenu(
                list_comics,
                numbered=True,
                prompt='Выберете комикc:\n',
                blank=True
            )
            return choose_comic
        return ''

    def add_chapter(self):
        comic = self.choose_comic()
        if not comic:
            return CANCEL
        repeat = pyip.inputInt(
            prompt='Сколько частей создать?\n',
            blank=True,
            min=1
        )
        if not repeat:
            return CANCEL
        comic = Comic(self.path / comic)
        comic.add_chapter(repeat)
        if int(repeat) == 1:
            return 'Новая часть и подпапки созданы.'
        else:
            return f'Новые части ({repeat}) и подпапки созданы.'

    def extract_image(self):
        comic = self.choose_comic()
        if not comic:
            return CANCEL
        comic = Comic(self.path / comic)
        comic.extract_image()
        return 'Изображения извлечены.'
