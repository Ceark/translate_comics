import os
import shutil
from pathlib import Path
from typing import List

import bs4
import pyinputplus as pyip
import send2trash
from PIL import Image
from win32com.client import Dispatch

from site_and_selectors import SETTINGS


def number_string(name: str):
    """
    Возвращает строку, состояющую из первых чисел полученной строки.
    """
    number = ''
    for symbol in name:
        if not symbol.isdecimal():
            break
        number += symbol
    return number


def search_htm_file(chapter: Path):
    """
    Перебирает файлы папки в поисках .htm-файла и, если рядом с ним
    есть папка с подходящим названием, возвращает путь файла
    и путь папки.
    """
    for directory, folders, files in os.walk(chapter):
        for file in [
            Path(file) for file
            in files
            if '.htm' in Path(file).suffix
        ]:
            site_dir = Path(directory, file.stem + '_files')
            if site_dir.exists():
                site_file = Path(directory, file)
                return (site_file, site_dir)
    return (False, False)


def list_image(
    example_soup: bs4.BeautifulSoup,
    site_dir: Path
):
    """
    Возвращает список путей к файлам изображений.

    Возможные исключения (вернёт False):
        - в файле нет тэга <link>'
        - сайта нет в списке обрабатываемых
        - нет подходящего селектора
        - не хватает нескольких файлов изображений
    """
    if example_soup.link:  # у сайта нет тэга <link>
        link = example_soup.link.attrs['href']
        for site in SETTINGS:
            if site in link:  # сайта нет в списке обрабатываемых
                func = SETTINGS[site]['function']
                parameters = SETTINGS[site]['parameters']
                # names_images: (list[str] | list)
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
    """
    Копированиe файлов изображений в заданную папку,
    изображения будут переименованы.
    """
    for index, file in enumerate(image_path, 1):
        new_name: str = str(index) + file.suffix
        shutil.copy(
            file,
            target / new_name
        )


def unite(image_path: List[Path], target: Path):
    """
    Вертикальноe объединение изображений.

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


def shortcut(target_path: str, shortcut_path: str, working_dir: str):
    """
    Функция создания ярлыка.

    - target_path - файл, для которого создаётся ярлык;
    - shortcut_path - адрес ярлыка;
    - working_dir - путь к папке, в которой лежит файл.
    """

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.WorkingDirectory = working_dir
    shortcut.save()
