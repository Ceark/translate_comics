import os
from pathlib import Path

import bs4
import pyinputplus as pyip
import send2trash

from additional_functions import (extract, list_image, number_string,
                                  search_htm_file, shortcut, unite)
from constants import CANCEL, NAME_CHAPTER, PAINT_SUFFIX
from extract_env import (ADDITIONAL, DELETE, EDITOR, LENGTH_NUMBER, NAMED_DIRS,
                         ORIGINAL, TRANSLATE)


class Folder:
    directories = NAMED_DIRS + ADDITIONAL

    def __init__(self, path: Path):
        self.path = path


class Comic(Folder):
    def _list_chapters_(self):
        """
        Получить список глав комикса.

        Глава комикса - любая папка, имя которой начинается с числа и не входит
        в список self.directories.
        """
        chapters = [
            chapter
            for chapter in self.path.iterdir()
            if (
                chapter.name not in self.directories
                and chapter.name[0].isdecimal()
                and chapter.is_dir()
            )
        ]
        return chapters

    def self_create(self):
        """Создать папку комикса и подпапки для него."""
        for directory in self.directories:
            (self.path / directory).mkdir(parents=True, exist_ok=True)

    def add_chapter(self, repeat: int):
        """Добавить нумерованную главу в комикс."""
        chapters = self._list_chapters_()
        name = max(chapters).name if chapters else '0'
        number = int(number_string(name)) + 1
        for number_chapter in range(number, number + repeat):
            long_number = str(number_chapter).rjust(LENGTH_NUMBER, '0')
            for directory in self.directories:
                (self.path / long_number / directory).mkdir(parents=True)

    def extract_image(self, method):
        """
        Извлекает и/или объединяет изображения первого найденного сайта
        и помещает результат в папку 'ORIGINAL'.
        """

        action = {
            'Извлечь': extract,
            'Соединить': unite
        }
        for chapter in self._list_chapters_():
            site_file, site_dir = search_htm_file(chapter)
            if site_dir:
                with open(site_file, "r", encoding="utf-8") as file:
                    example_soup = bs4.BeautifulSoup(
                        file.read(),
                        'html.parser'
                    )
                image_path = list_image(example_soup, site_dir)
                if image_path:
                    target = chapter / ORIGINAL
                    target.mkdir(exist_ok=True)
                    action[method](image_path, target)
                    if DELETE:
                        send2trash.send2trash([site_dir, site_file])
                else:
                    print(
                        f'Не удалось обработать папку {site_dir}.'
                        'Возможные причины:',
                        '- в файле нет тэга <link>;',
                        '- сайта нет в списке обрабатываемых;',
                        '- нет подходящего селектора;',
                        '- не хватает нескольких файлов изображений;'
                    )

    def move_images(self):
        """
        Перемещение изображений с расширениями Paint из папки EDITOR в папку
        TRANSLATE.
        """
        for chapter in self._list_chapters_():
            editor = chapter / EDITOR
            if editor.exists():
                translate = chapter / TRANSLATE
                translate.mkdir(exist_ok=True)
                list_files = [
                    file for file
                    in editor.iterdir()
                    if file.suffix in PAINT_SUFFIX
                ]
                for file in list_files:
                    target = translate / file.name
                    os.replace(file, target)

    def create_shortcut(self, folder: str):
        """
        Создание ярлыков для файлов папки части с указанными именем.

        Если передано пустое значение, то будут обработаны файлы,
        не упакованные в папки.
        """
        shortcut_folder = self.path / folder
        shortcut_folder.mkdir(exist_ok=True)
        folder = '' if folder == NAME_CHAPTER else folder
        for chapter in self._list_chapters_():
            num_chapter = number_string(chapter.name)
            path_folder = self.path / chapter / folder
            if path_folder.exists():
                files = [
                    file for file in path_folder.iterdir()
                    if file.is_file()
                ]
                for file in files:
                    name_shortcut = num_chapter + '_' + file.stem + '.lnk'
                    target_path = str(file)
                    shortcut_path = str(shortcut_folder / name_shortcut)
                    working_dir = str(file.parent)
                    shortcut(
                        target_path=target_path,
                        shortcut_path=shortcut_path,
                        working_dir=working_dir
                    )

    def update_folder(self):
        """
        Добавить в папки комикса и частей, все директории.

        Предназначение: на случай изменения настроек.
        """
        for folder in ([self.path] + self._list_chapters_()):
            for directory in self.directories:
                (folder / directory).mkdir(parents=True, exist_ok=True)


def choose_comic(func):
    """
    Декоратор для выбора комикса.

    Получив объект MainFolder, функция формирует список из имён находящихся в
    нём папок, после чего пользователь выбирает нужную папку (комикс). Путь к
    выбранному комиксу передается в декорированную функцию. Если выбирать
    не из чего или пользователь выбрал ничего, функция вернёт строку отмены.
    """
    def wrapper(self: 'MainFolder'):
        list_comics = [
            value.name for value
            in self.path.iterdir()
            if value.is_dir()
        ]
        if list_comics:
            choose_comic = pyip.inputMenu(
                list_comics,
                numbered=True,
                prompt='Выберете комикc:\n',
                blank=True
            )
            if choose_comic:
                path_comic = self.path / choose_comic
                result = func(self, path_comic)
                return result
        return CANCEL
    return wrapper


class MainFolder(Folder):
    def create_comic(self):
        """
        Создание комикса.

        Пользователь вводит название комикса, если оно валидно, то будет отдана
        команда о создании комикса.
        Пустое значение - действие отменяется.
        """
        blockRegexes = [
            (
                r'\.$',
                'Точка не может стоять в конце названия папки.'
            ),
            (
                r'[:<>"\/\\\|\?\*]',
                'В названии папки использованы недопустимые символы.'
            )
        ]
        if os.listdir(self.path):
            blockRegexes.append(
                (
                    '|'.join(os.listdir(self.path)),
                    'Папка с таким названием уже существует.'
                )
            )
        name_new_comic = pyip.inputStr(
            prompt='Название нового комикса: ',
            blockRegexes=blockRegexes,
            blank=True
        )
        if name_new_comic:
            comic = Comic(path=self.path / name_new_comic)
            comic.self_create()
            return f'Создана папка для комикса "{name_new_comic}".'
        return CANCEL

    @choose_comic
    def add_chapter(self, path_comic):
        """
        Добавить часть(-и) к комиксу.
        """
        repeat = pyip.inputInt(
            prompt='Сколько частей создать?\n',
            blank=True,
            min=1
        )
        if not repeat:
            return CANCEL
        comic = Comic(path_comic)
        comic.add_chapter(repeat)
        return f'Новые части ({repeat}) и подпапки созданы.'

    @choose_comic
    def extract_image(self, path_comic):
        """
        Извлечь изображения.
        """
        comic = Comic(path_comic)
        method = pyip.inputMenu(
            choices=[
                'Извлечь',
                'Соединить'
            ],
            prompt='Что делать с изображениями?\n',
            numbered=True,
            blank=True
        )
        if method:
            comic.extract_image(method)
            return 'Процесс завершен.'
        return CANCEL

    @choose_comic
    def move_images(self, path_comic):
        comic = Comic(path_comic)
        comic.move_images()
        return 'Изображения перемещены.'

    @choose_comic
    def create_shortcut(self, path_comic):
        """
        Создать ярлыки для файлов в папках части комикса, ярлыки будут
        расположены в папках комикса для ярлыков.

        Если выбрано 'Для файлов папки', то ярлыки будут созданы для файлов,
        находящихся непосредственно в папке части.
        """
        comic = Comic(path_comic)
        word_folder = ('Для файлов папки',)
        choices = self.directories + word_folder
        while True:
            folder = pyip.inputMenu(
                choices=choices,
                prompt='Для файлов какой подпапки создать ярлыки?\n',
                blank=True,
                numbered=True
            )
            if folder:
                folder = NAME_CHAPTER if folder in word_folder else folder
                comic.create_shortcut(folder)
                return 'Ярлыки созданы (или перезаписаны).'
            else:
                break
        return CANCEL

    @choose_comic
    def update_folder(self, path_comic):
        comic = Comic(path_comic)
        comic.update_folder()
        return 'Подпапки созданы.'
