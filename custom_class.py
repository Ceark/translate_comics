import os
import shutil
from pathlib import Path

import bs4
import pyinputplus as pyip

from extract_env import LENGTH_NUMBER, directories_chapter, directories_comic

CANCEL = 'Действие отменено.'


class Comic:
    dir_comic = directories_comic()
    dir_chapters = directories_chapter()
    length_number = int(LENGTH_NUMBER) if LENGTH_NUMBER.isdecimal() else 2

    def __init__(self, path):
        self.path = Path(path)

    def self_create(self):
        os.mkdir(self.path)
        for directory in self.dir_comic.values():
            os.mkdir(self.path / directory)

    def list_chapters(self):
        chapters = [
            chapter for chapter in os.listdir(self.path) if (
                chapter not in self.dir_chapters.values()
                and Path(self.path, chapter).is_dir()
            )
        ]
        return chapters

    def add_chapter(self, repeat):
        chapters = self.list_chapters()
        number = max(chapters) if chapters else '0'
        if not number.isdecimal():
            number = number.split('_')[0]
            if not number.isdecimal():
                number = len(chapters)
        number = int(number) + 1
        for number_chapter in range(number, number + repeat):
            long_number = str(number_chapter).rjust(self.length_number, '0')
            for directory in self.dir_chapters.values():
                os.makedirs(Path(self.path, long_number, directory))

    def extract_image(self):
        chapters = self.list_chapters()
        for chapter in chapters:
            # Поиск файла сайта и папки с содержимым
            path = self.path / chapter / self.dir_chapters['original']
            if not path.exists():
                continue
            flag = {
                'file': False,
                'directory': False
            }
            for value in os.listdir(path):
                if Path(path, value).is_dir():
                    path_site_dir = Path(path, value)
                    flag['directory'] = True
                elif Path(path, value).is_file():
                    path_site_file = Path(path, value)
                    flag['file'] = True
            if not (flag['directory'] and flag['file']):
                continue
            # Экстракция изображений
            example_file = open(path_site_file, "r", encoding="utf-8")
            example_soup = bs4.BeautifulSoup(example_file.read(), 'html.parser')
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
            # Удаление флагов
            del (path_site_dir, path_site_file)


class MainFolder:
    def __init__(self, path):
        self.path = Path(path)

    def create_comic(self):
        blockRegexes = [
            ('|'.join(os.listdir(self.path)),
             'Папка с таким названием уже существует.'),
            (r'\.$', 'Точка не может стоять в конце названия.'),
            (r'[:<>"\/\\\|\?\*]',
             'В названии использованы недопустимые символы.')
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
            value for value in os.listdir(self.path) if Path(
                self.path / value
            ).is_dir()
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
