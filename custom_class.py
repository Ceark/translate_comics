import os
import shutil
from pathlib import Path
from typing import List

import bs4
import pyinputplus as pyip
import send2trash
from PIL import Image
from win32com.client import Dispatch

from extract_env import (ADDITIONAL, DELETE, EDITOR, LENGTH_NUMBER, ORIGINAL,
                         TRANSLATE)

CANCEL = 'Действие отменено.'


class Comic:
    directories = ADDITIONAL + [ORIGINAL, EDITOR, TRANSLATE]

    def __init__(self, path: Path):
        self.path = path

    def self_create(self):
        """Создать папку и подпапки для комикса."""

        for directory in self.directories:
            (self.path / directory).mkdir(parents=True)

    def list_chapters(self):
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

    def number_chapter(self, name: str):
        """
        Принимает строку и возвращает строку, состояющую из первых чисел
        полученной Зстроки.
        """

        number = ''
        for symbol in name:
            if not symbol.isdecimal():
                break
            number += symbol
        return number

    def add_chapter(self, repeat: int):
        """
        Добивить нумерованную часть.

        Определят часть с самым большим номером после чего создает часть
        с номером +1. Параметр "repeat" - количество добавленных частей.
        """

        chapters = self.list_chapters()
        name = max(chapters).name if chapters else '0'
        number = int(self.number_chapter(name)) + 1
        for number_chapter in range(number, number + repeat):
            long_number = str(number_chapter).rjust(LENGTH_NUMBER, '0')
            for directory in self.directories:
                (self.path / long_number / directory).mkdir(parents=True)

    def extract_image(self, method):
        """Извлекает и объединяет изображения из части комикса."""

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
                    site_file = directory / file
                    site_dir = directory / (file.stem + '_files')
                    if site_dir.exists():
                        return (site_file, site_dir)
            return (False, False)

        def image_names(example_soup: bs4.BeautifulSoup):
            """
            Функция для извлечения списка имен файлов.

            После опознания сайта по <link> передает в подфунцкию (используют
            ли разные сайты разный подход?) файл и параметры.
            """
            def extract_one(
                example_soup: bs4.BeautifulSoup,
                selectors: list[str],
                tag: str,
                symbol: str
            ):
                for selector in selectors:
                    parts = example_soup.select(selector)
                    if parts:
                        elems: list[str] = [
                            child.attrs[tag] for child
                            in parts[0].children
                            if isinstance(child, bs4.element.Tag)
                        ]
                        elems = [
                            Path(value).name.partition(symbol)[0]
                            for value in elems
                        ]
                        return elems
                    return []

            if example_soup.link:
                link = example_soup.link.attrs['href']
                tapas = [
                    'article[class="viewer__body js-episode-article main__body"]',
                    'article[class="viewer__body js-episode-article main__body hidden js-mature-content"]'
                ]
                webtoons = [
                    'div[class="viewer_img _img_viewer_area"]'
                ]
                name_sites = {
                    'tapas': 'tapas',
                    'webtoons': 'webtoons'
                }
                parameters = {
                    name_sites['tapas']: {
                        'selectors': tapas,
                        'tag': 'data-src',
                        'symbol': '*'
                    },
                    name_sites['webtoons']: {
                        'selectors': webtoons,
                        'tag': 'data-url',
                        'symbol': '?'
                    }
                }
                func = {
                    name_sites['tapas']: extract_one,
                    name_sites['webtoons']: extract_one
                }
                for site in name_sites:
                    if site in link:
                        elems = func[site](example_soup, **parameters[site])
                        return elems
            return False

        def list_image_files(site_dir: Path, elems: list[str]):
            """
            Фунцкия составляет список путей файлов изображений комикса.
            Если какое-то изображение не сущесвует, вернет False.
            """
            image_path = [
                site_dir / value for value
                in elems
                if (site_dir / value).exists()
            ]
            if len(image_path) == len(elems):
                return image_path
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

        for chapter in self.list_chapters():
            site_file, site_dir = search_file(chapter)
            if site_dir:
                with open(site_file, "r", encoding="utf-8") as file:
                    example_soup = bs4.BeautifulSoup(
                        file.read(),
                        'html.parser'
                    )
                elems = image_names(example_soup)
                image_path = list_image_files(site_dir, elems)
                if image_path:
                    action = {
                        'Извлечь': extract,
                        'Соединить': unite
                    }
                    target = Path(chapter / ORIGINAL)
                    target.mkdir(exist_ok=True)
                    action[method](image_path, target)
                    if DELETE:
                        send2trash.send2trash([site_dir, site_file])
                else:
                    print(
                        f'В папке {site_dir} не хватает некоторых изображений.',
                        'Пожалуйста, загрузите файл сайта заново.'
                    )

    def create_shortcut(self, folder_name: str):
        """
        Создание ярлыков для файлов папки с указанными именем.

        Если передано пустое значение, то будут обработаны файлы,
        не упакованные в папки.
        """

        def shortcut(target_path: str, shortcut_path: str, working_dir: str):
            """Функция создания ярлыка."""

            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target_path
            shortcut.WorkingDirectory = working_dir
            shortcut.save()

        shortcut_folder = (
            self.path / folder_name if folder_name else self.path / 'Разное'
        )
        shortcut_folder.mkdir(exist_ok=True)
        for chapter in self.list_chapters():
            number = self.number_chapter(chapter.name) + '_'
            path_folder = self.path / chapter / folder_name
            if path_folder.exists():
                files = [
                    file for file in path_folder.iterdir()
                    if file.is_file()
                ]
                for file in files:
                    shortcut_path = str(
                        shortcut_folder / (number + file.stem + '.lnk')
                    )
                    working_dir = str(file.parent)
                    target_path = str(file)
                    shortcut(
                        target_path=target_path,
                        shortcut_path=shortcut_path,
                        working_dir=working_dir
                    )


class MainFolder:
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

    def choose_comic(self):
        """
        Выбор комикса.

        Возвращает имя выбранной папки из списка папок, находящихся
        в self.path
        """
        list_comics = [
            value.name for value in self.path.iterdir()
            if value.is_dir()
        ]
        if list_comics:
            choose_comic = pyip.inputMenu(
                list_comics,
                numbered=True,
                prompt='Выберете комикc:\n',
                blank=True
            )
            return choose_comic
        return False

    def add_chapter(self):
        """
        Добавить часть.

        Пользователь выбирает комикс, вводит число, если есть оба значения, то
        будет отдана команда о добавлении части(-ей).
        Пустое значение - действие отменяется.
        """
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
        if repeat == 1:
            return 'Новая часть и подпапки созданы.'
        else:
            return f'Новые части ({repeat}) и подпапки созданы.'

    def extract_image(self):
        """
        Извлечь изображения.

        Пользователь выбирает комикс, выбирает метод, отдается приказ об
        извлечении изображений.
        Пустое значение - действие отменяется.
        """
        comic = self.choose_comic()
        if comic:
            comic = Comic(self.path / comic)
            method = pyip.inputMenu(
                choices=[
                    'Извлечь',
                    'Соединить'
                ],
                prompt='Что делать с изображениями:\n',
                numbered=True,
                blank=True
            )
            if method:
                comic.extract_image(method)
                return 'Процесс завершен.'
        return CANCEL

    def create_shortcut(self):
        """
        Извлечь изображения.

        Пользователь выбирает комикс, выбирает метод, отдается приказ об
        извлечении изображений.
        Пустое значение - действие отменяется.
        """
        comic = self.choose_comic()
        if comic:
            comic = Comic(self.path / comic)
            word_folder = 'Для файлов папки'
            choices = [
                value.name for value in comic.path.iterdir()
                if value.name in comic.directories
            ] + [word_folder]
            while True:
                folder = pyip.inputMenu(
                    choices=choices,
                    prompt='Для файлов какой подпапки создать ярлыки?\n',
                    blank=True,
                    numbered=True
                )
                if folder:
                    folder = '' if folder == word_folder else folder
                    comic.create_shortcut(folder)
                else:
                    break
        return CANCEL

    def move_images(self):
        pass
        # comic = self.choose_comic()
        # if comic:

        # return CANCEL

# Новая система определения сайта (выполнено)
# Поиск файлов во сайтов во всех папках главы комикса (выполнено)
# Добавить нумерацию файлов Union (выполнено)
# Перемещение новых файлов из папки Photoshop в папку Перевод

# Добавить декоратор @choose_comic
