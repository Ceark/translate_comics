import os
import shutil
from pathlib import Path
from typing import Callable, List, Literal

import bs4
import pyinputplus as pyip
import send2trash
from PIL import Image
from win32com.client import Dispatch

from custom_typing import PythonSettings


def extract_one(
    example_soup: bs4.BeautifulSoup,
    site_dir: Path,
    selectors: list,
    tag: str,
    symbol: str
):
    """
    Возвращает список имен файлов.
    """
    for selector in selectors:
        parts = example_soup.select(selector)  # нет подходящего селектора
        if parts:
            for part in parts:
                elems: list = [
                    str(child.attrs[tag]) for child
                    in part.children
                    if isinstance(child, bs4.element.Tag)
                ]
                elems = [
                    Path(value).name.partition(symbol)[0]
                    for value in elems
                ]
                validate = [  # не хватает нескольких файлов изображений
                    (site_dir / file).exists()
                    for file in elems
                ]
                if False not in validate:
                    return elems
    return []


def extract(images: list[Path], target: Path):
    for index, file in enumerate(images, 1):
        name_file: str = str(index) + file.suffix
        shutil.copy(file, target / name_file)


def unite(images: list[Path], target: Path):
    width, height = 0, 0
    coordinates = [(width, height)]
    # Получить кортежи координат
    for file in images:
        with Image.open(file) as img:
            height += img.height
            coordinates.append((width, height))
    # Получить ширину изображения
    with Image.open(file) as img:
        width = img.width
    # Создание единого изображения
    with Image.new('RGB', (width, height)) as new_img:
        for index, file in enumerate(images):
            with Image.open(file) as img:
                copy_img = img.copy()
                new_img.paste(copy_img, coordinates[index])
                copy_img.close()
        new_img.save(target / f'{target.parts[-2]}_Union.png')
    pass


def search_htm_file(chapter: Path):
    """
    Перебирает файлы папки в поисках .htm-файла и, если рядом с ним
    есть папка с подходящим названием, возвращает путь файла
    и путь папки.
    """
    for directory, folders, files in chapter.walk():
        htm_files = [
            Path(file) for file
            in files
            if '.htm' in Path(file).suffix
        ]
        for file in htm_files:
            if file.stem + '_files' in folders:
                return {
                    'dir': directory / (file.stem + '_files'),
                    'file': directory / file
                }


def list_chapters(folder: Path, settings: PythonSettings):
    exclusion = [
        settings['original'],
        settings['editor'],
        settings['translate']
    ] + [
        string.strip()
        for string
        in ','.split(settings['other_folder'])
    ]
    chapters = [
        subfolder
        for subfolder
        in folder.iterdir()
        if (
            subfolder.is_dir()
            and subfolder.name not in exclusion
            and subfolder.name[0].isdecimal()
        )
    ]
    return chapters


def list_images(htm_file: Path, folder: Path, site_and_selectors: dict):
    with open(htm_file, "r", encoding="utf-8") as file:
        example_soup = bs4.BeautifulSoup(
            file.read(),
            'html.parser'
        )
    link = example_soup.link.attrs['href']
    site_and_selectors.get(link)
    pass


def command_extract_image(
        comic: str, function: Callable, settings: PythonSettings
):
    folder = Path(settings['base_dir'], comic)
    chapters = list_chapters(folder, settings)
    for chapter in chapters:
        pass
