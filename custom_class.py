import os
import shutil
from pathlib import Path
from typing import List

import bs4
import pyinputplus as pyip
import send2trash
from PIL import Image
from win32com.client import Dispatch

from extract_env import (ADDITIONAL, DELETE, EDITOR, LENGTH_NUMBER, NAMED_DIRS,
                         ORIGINAL, TRANSLATE)
from site_and_selectors import SETTINGS

CANCEL = 'Действие отменено.'


class Comic:
    directories = ADDITIONAL + NAMED_DIRS

    def __init__(self, path: Path):
        self.path = path

    def self_create(self):
        """Создать папку и подпапки для комикса."""

        for directory in self.directories:
            (self.path / directory).mkdir(parents=True, exist_ok=True)

    def _list_chapters_(self):
        """
        Получить список путей глав комикса.

        Главой комикса является любая папка, имя которой начинается с числа
        и не входит в список self.directories.
        """

        chapters = [
            chapter for chapter in self.path.iterdir()
            if (
                chapter.name not in self.directories
                and chapter.name[0].isdecimal()
                and chapter.is_dir()
            )
        ]
        return chapters

    def _number_chapter_(self, name: str):
        """
        Возвращает строку, состояющую из первых чисел полученной строки.
        """

        number = ''
        for symbol in name:
            if symbol.isdecimal():
                number += symbol
            else:
                break
        return number

    def add_chapter(self, repeat: int):
        """
        Добавить нумерованную часть.

        Определяет часть с самым большим номером, после чего создает часть
        с номером +1. Параметр "repeat" - количество добавленных частей.
        """

        chapters = self._list_chapters_()
        name = max(chapters).name if chapters else '0'
        number = int(self._number_chapter_(name)) + 1
        for number_chapter in range(number, number + repeat):
            long_number = str(number_chapter).rjust(LENGTH_NUMBER, '0')
            for directory in self.directories:
                (self.path / long_number / directory).mkdir(parents=True)

    def extract_image(self, method):
        """
        Извлекает и/или объединяет изображения первого найденного сайта
        и помещает результат в папку 'ORIGINAL'.
        """

        def search_file(chapter: Path):
            """
            Перебирает файлы папки в поисках .htm-файла и, если рядом с ним
            есть папка с подходящим названием, возвращает их пути,
            файл и папку.
            """
            for directory, folders, files in chapter.walk():
                for file in [
                    Path(file) for file
                    in files
                    if '.htm' in Path(file).suffix
                ]:
                    site_dir = directory / (file.stem + '_files')
                    if site_dir.exists():
                        site_file = directory / file
                        return (site_file, site_dir)
            return (False, False)

        def list_image(
            example_soup: bs4.BeautifulSoup,
            site_dir: Path
        ):
            if example_soup.link:
                link = example_soup.link.attrs['href']
                for site in SETTINGS:
                    if site in link:
                        func = SETTINGS[site]['function']
                        parameters = SETTINGS[site]['parameters']
                        names_images: list[str] = func(
                            example_soup, site_dir, **parameters
                        )
                        images_path = [
                            site_dir / value for value
                            in names_images
                            if (site_dir / value).exists()
                        ]
                        if len(images_path) == len(names_images):
                            return images_path
            return False

        def extract(image_path: List[Path], target: Path):
            """Функция для копирования файла изображения в заданную папку."""

            for index, file in enumerate(image_path, 1):
                new_name: str = str(index) + file.suffix
                shutil.copy(
                    file,
                    target / new_name
                )

        def unite(image_path: List[Path], target: Path):
            """
            Функция для вертикального объединения изображений.

            Предполагается, что первое изображение - самое широкое. Будет
            создано изображение Union.png в целевой папке.
            """

            width, height = 0, 0
            coordinates = [(width, height)]
            # Получить кортежи координат
            for file in image_path:
                with Image.open(file) as img:
                    height += img.height
                    coordinates.append((width, height))
            # Получить ширину изображения
            with Image.open(file) as img:
                width = img.width
            # Создание единого изображения
            with Image.new('RGB', (width, height)) as new_img:
                for index, file in enumerate(image_path):
                    with Image.open(file) as img:
                        copy_img = img.copy()
                        new_img.paste(copy_img, coordinates[index])
                        copy_img.close()
                new_img.save(target / f'{target.parts[-2]}_Union.png')

        action = {
            'Извлечь': extract,
            'Соединить': unite
        }
        for chapter in self._list_chapters_():
            site_file, site_dir = search_file(chapter)
            if site_dir:
                with open(site_file, "r", encoding="utf-8") as file:
                    example_soup = bs4.BeautifulSoup(
                        file.read(),
                        'html.parser'
                    )
                image_path = list_image(example_soup, site_dir)
                if image_path:
                    target = Path(chapter / ORIGINAL)
                    target.mkdir(exist_ok=True)
                    action[method](image_path, target)
                    if DELETE:
                        send2trash.send2trash([site_dir, site_file])
                else:
                    print(
                        f'В папке {site_dir} не хватает изображений.',
                        'Пожалуйста, загрузите файл сайта заново.'
                    )

    def create_shortcut(self, folder_name: str):
        """
        Создание ярлыков для файлов папки части с указанными именем.

        Если передано пустое значение, то будут обработаны файлы,
        не упакованные в папки. Ярлыки будут расположены в папке комикса.
        """

        def shortcut(target_path: str, shortcut_path: str, working_dir: str):
            """
            Функция создания ярлыка.

            shortcut_path - адрес ярлыка;
            target_path - файл, для которого создаётся ярлык;
            working_dir - путь к папке, в которой лежит файл.
            """

            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target_path
            shortcut.WorkingDirectory = working_dir
            shortcut.save()

        shortcut_folder = self.path / folder_name
        shortcut_folder.mkdir(exist_ok=True)
        for chapter in self._list_chapters_():
            num_chapter = self._number_chapter_(chapter.name)
            path_folder = self.path / chapter / folder_name
            if path_folder.exists():
                files = [
                    file for file in path_folder.iterdir()
                    if file.is_file()
                ]
                for file in files:
                    name_shortcut = num_chapter + '_' + file.stem + '.lnk'
                    shortcut_path = str(shortcut_folder / name_shortcut)
                    working_dir = str(file.parent)
                    target_path = str(file)
                    shortcut(
                        target_path=target_path,
                        shortcut_path=shortcut_path,
                        working_dir=working_dir
                    )

    def move_images(self):
        """
        Перемещение изображений с расширениями Paint из папки EDITOR в папку
        TRANSLATE.
        """
        for chapter in self._list_chapters_():
            path_editor = chapter / EDITOR
            if path_editor.exists():
                path_translate = chapter / TRANSLATE
                path_translate.mkdir(exist_ok=True)
                list_files = [
                    file for file
                    in path_editor.iterdir()
                    if file.suffix in (
                        '.png',
                        '.bmp',
                        '.dip',
                        '.jpg',
                        '.jpeg',
                        '.jpe',
                        '.jfif',
                        '.gif',
                        '.tif',
                        '.tiff',
                        '.heic',
                        '.hif',
                        '.paint'
                    )
                ]
                for file in list_files:
                    file.move(path_translate)

    def create_folder(self):
        for chapter in self._list_chapters_():
            for name in self.directories:
                (chapter / name).mkdir(exist_ok=True)
            number_chapter = self._number_chapter_(chapter.name)
            if len(number_chapter) < LENGTH_NUMBER:
                number = number_chapter.rjust(LENGTH_NUMBER, '0')
                name = chapter.name[len(number_chapter):]
                new_name = chapter.parent / (number + name)
                chapter.rename(new_name)


def choose_comic(func):
    """
    Декоратор для выбора комикса.

    Получив объект MainFolder, функция формирует список из имён находящихся в
    нём папок, после чего пользователь выбирает нужную папку (комикс). Путь к
    выбранному комиксу передается в декорированную функцию. Если выбирать
    не из чего или пользователь выбрал ничего, функция вернёт строку отмены.
    """
    def wrapper(self: MainFolder):
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


class MainFolder:
    directories = NAMED_DIRS + ADDITIONAL

    def __init__(self, path: Path):
        self.path = path

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

        Если пользователь не выбрал число (сколько частей добавлять), то
        действие отменяется.
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

        Если пользователь не выбрал метод, действие отменяется.
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
                folder = 'Разное' if folder == word_folder else folder
                comic.create_shortcut(folder)
                return 'Ярлыки созданы (или перезаписаны).'
            else:
                break
        return CANCEL

    @choose_comic
    def move_images(self, path_comic):
        comic = Comic(path_comic)
        comic.move_images()
        return 'Изоюражения перемещены.'

    @choose_comic
    def create_folder(self, path_comic):
        comic = Comic(path_comic)
        comic.create_folder()
        return 'Подпапки созданы, номера частей стандартизированы.'
