import os
import shutil
from pathlib import Path
from typing import List

import bs4
import pyinputplus as pyip
import send2trash
from PIL import Image
from win32com.client import Dispatch

from extract_env import ADDITIONAL, DELETE, LENGTH_NUMBER, ORIGINAL

CANCEL = 'Действие отменено.'


class Comic:
    directories = ADDITIONAL + [ORIGINAL]

    def __init__(self, path: Path):
        self.path = path

    def self_create(self):
        """Создать папку и подпапки для комикса."""

        for directory in self.directories:
            (self.path / directory).mkdir(parents=True)

    def list_chapters(self):
        """
        Получить список путей глав комикса.

        Главой комикса является любая папка, имя которой начинается с числа,
        не входит в список self.directories.
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
        полученной строки.
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
        """Извлекает и объединяет изображения из папки комикса."""

        def search_dir(folder: Path):
            """
            Перебирает файлы .htm и, если рядом с файлом есть папка
            с подходящим названием, возвращает их пути.
            """

            site_file, site_dir = False, False
            if folder.exists():
                for file in [
                    _ for _ in folder.iterdir()
                    if _.is_file()
                    and '.htm' in _.suffix
                ]:
                    name_dir = file.stem + '_files'
                    if file.with_name(name_dir).exists():
                        site_dir = file.with_name(name_dir)
                        site_file = file
                        break
            return (site_file, site_dir)

        def image_names(example_soup: bs4.BeautifulSoup):
            """
            Функия опознает сайт и извлекает список имен файлов.

            Опозанание происходит по первому тэгу <link>. Если тэг отсутсвует
            или опозание не удалось, возвращает кортеж с текстом ошибки.
            """
            def tapas_webtoons(
                example_soup: bs4.BeautifulSoup,
                selector: str,
                tag: str,
                symbol: str
            ):
                parts = example_soup.select(selector)
                if parts:
                    elems = [
                        child for child
                        in parts[0].children
                        if not child == '\n'
                    ]
                    elems = [
                        Path(value.attrs[tag]).name.partition(symbol)[0]
                        for value in elems
                    ]
                    return elems
                return []

            if example_soup.link is not None:
                link = example_soup.link.attrs['href']
                websites = {
                    'tapas': {
                        'function': tapas_webtoons,
                        'parameters': {
                            'selector': 'article[class="viewer__body js-episode-article main__body"]',
                            'tag': 'data-src',
                            'symbol': '*'
                        }
                    },
                    'webtoons': {
                        'function': tapas_webtoons,
                        'parameters': {
                            'selector': 'div[class="viewer_img _img_viewer_area"]',
                            'tag': 'data-url',
                            'symbol': '?'
                        }
                    }
                }
                for site in websites:
                    if site in link:
                        parameters = websites[site]['parameters']
                        func = websites[site]['function']
                        elems = func(example_soup, **parameters)
                        return elems
                return False

        def list_image_files(site_dir: Path, elems):
            """
            Составить список путей файлов изображений комикса.
            Если какое-то изображение не сущесвует, вернет False.
            """

            image_path = [
                site_dir / value for value in elems
            ]
            for path in image_path:
                if not path.exists():
                    return False
            return image_path

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

            Прежполагается, что первое изображение - самое широкое. Будет
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
                new_img.save(target / 'Union.png')

        for chapter in self.list_chapters():
            original = chapter / ORIGINAL
            site_file, site_dir = search_dir(original)
            if site_dir and site_file:
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
                    action[method](image_path, original)
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
