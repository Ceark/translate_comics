import json
import shutil
from pathlib import Path
from typing import Callable, TypedDict

import bs4
from PIL import Image


class PythonSettings(TypedDict):
    base_dir: str
    original: str
    editor: str
    translate: str
    other_folder: str
    delete: bool
    length_number: int


class Site():
    def __init__(self, path: Path):
        with open(path, 'r', encoding='utf-8') as file:
            json_file = json.load(file)
        self.name_site = json_file['name_site']
        self.selectors = json_file['selectors']
        self.tag = json_file['tag']
        self.symbol = json_file['symbol']


def extract_one(
        example_soup: bs4.BeautifulSoup,
        site: Site
):
    """
    Функция по извлечению имен файлов изображений из файла сайта.

    Получив htnm-файл, функция берёт селектор,
    в котором должны храниться изображения, и вырезает все появления этого
    селектора (parts). Потом в она разбирает эти части (part), смотрит на
    их вложения и вырезает ту часть, в которой содержится имя файла
    изображения, после чего извлекает оттуда имя файла изображения;
    предполагается, что оно хранится в следующем формате:
    имя файла + символ + какой-то текст.

    В итоге функция вернет только имена из первого селектора.
    """
    for selector in site.selectors:
        parts = example_soup.select(selector)
        for part in parts:
            elems = [
                str(child.attrs[site.tag])
                for child
                in part.children
                if isinstance(child, bs4.element.Tag)
            ]
            elems = [
                Path(value).name.partition(site.symbol)[0]
                for value
                in elems
            ]
            if elems:
                return elems


# Составить список глав комикса
def list_chapters(path: Path, technical_folder: list[str]):
    """
    Получить список глав папки.

    Глава - папка, имя которой начинается с числа и не входит в список
    технических папок.
    """
    chapters = [
        chapter
        for chapter
        in path.iterdir()
        if (
            chapter.is_dir()
            and chapter.name[0].isdecimal()
            and chapter.name not in technical_folder
        )
    ]
    return chapters


# Найти htm-файл и его папку
def search_htm_file(chapter: Path):
    for directory, folders, files in chapter.walk():
        for file in [
            Path(file)
            for file
            in files
            if '.htm' in Path(file).suffix
        ]:
            site_dir = Path(directory, file.stem + '_files')
            if site_dir.exists():
                site_file = Path(directory, file)
                return (site_file, site_dir)
    return (None, None)


# Определить сайт и получить "схему сайта"
def identify_site(
        example_soup: bs4.BeautifulSoup,
        site_and_selectors: Path = Path('.', 'site_and_selectors')
):
    if example_soup.link:
        link = example_soup.link.attrs['href']
        for file in [
            file
            for file
            in site_and_selectors.iterdir()
            if (
                file.is_file()
                and file.suffix == '.json'
            )
        ]:
            if file.stem in link:
                return Site(file)
    return None


# В соответствии со схемой, извлечь имена изображений
def name_image(site: bs4.BeautifulSoup, scheme: Site):
    for selector in scheme.selectors:
        parts = site.select(selector)
        for part in parts:
            elems = [
                Path(str(child.attrs[scheme.tag])).name.partition(scheme.symbol)[0]
                for child
                in part.children
                if isinstance(child, bs4.element.Tag)
            ]
            return elems
    return None


# Провести экстракцию
def general_extract(
        func: Callable, file_names: list[str],
        path_source: Path, path_target: Path
):
    path_images = [
        path_source / file
        for file
        in file_names
    ]
    validate = [
        file.exists()
        for file
        in path_images
    ]
    if not (False in validate):
        raise ValueError
    del validate
    path_target.mkdir(parents=True, exist_ok=True)
    func(image_path=path_images, target=path_target)


def orchestra(
        func_var: Callable,
        comic_path: Path,
        settings: PythonSettings
):
    technical_folder = [
        settings['editor'],
        settings['original'],
        settings['translate']
    ] + [
        i.strip()
        for i
        in settings['other_folder'].split(',')
    ]
    chapters = list_chapters(comic_path, technical_folder)
    for chapter in chapters:
        htm_file, htm_dir = search_htm_file(chapter)
        with open(htm_file, "r", encoding="utf-8") as file:
            example_soup = bs4.BeautifulSoup(
                file.read(),
                'html.parser'
            )
        site = identify_site(example_soup)
        if site is None:
            continue
        list_name_image = name_image(example_soup, site)
        general_extract(
            func=func_var,
            file_names=list_name_image,
            path_source=htm_dir,
            path_target=chapter / settings['original']
        )


def extract(image_path: list[Path], target: Path):
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


def unite(image_path: list[Path], target: Path):
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
