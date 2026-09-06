import json
import shutil
from pathlib import Path
from typing import Callable

import bs4
import send2trash
from PIL import Image

from custom_class.custom_class import Chapter
from custom_typing.custom_typing import Settings, SiteSelectors


def copy_images(images: list[Path], target: Path):
    """
    Копированиe файлов в заданную папку, файлы будут переименованы.
    """
    for index, image in enumerate(images, 1):
        new_name = str(index) + image.suffix
        shutil.copy(
            image,
            target / new_name
        )


def unite(images_path: list[Path], target: Path):
    """
    Объеденить изображения и сохранить в папку target.
    """
    width, height = 0, 0
    coordinates = [(0, height)]
    for image in images_path:
        with Image.open(image) as img:
            height += img.height
            coordinates.append((0, height))
    with Image.open(image) as img:
        width = img.width
    with Image.new('RGB', (width, height)) as union:
        for index, image in enumerate(images_path):
            with Image.open(image) as img:
                union.paste(img, coordinates[index])
        union.save(target / 'Union.png')


def key_max_chapters(path: Path):
    """
    Функция, с помощью которой можно получить номер главы комикса.

    Функция предназначена для вставки в поле 'key' функции max(),
    когда нужно выяснить наибольший номер главы комикса.
    """
    string = ''
    for symbol in path.name:
        if symbol.isdecimal():
            string += symbol
        else:
            return int(string)


def list_chapters(comic: Path, technical_folder: list[str]):
    """
    Получить список глав комикса.

    Глава комикса - любая папка, имя которой начинается с числа
    и не входит в список technical_folder.
    """
    chapters = [
        chapter
        for chapter
        in comic.iterdir()
        if (
            chapter.name not in technical_folder
            and chapter.name[0].isdecimal()
            and chapter.is_dir()
        )
    ]
    return chapters


def search_htm_files(comic: Path) -> list[tuple[Path, Path]]:
    """
    Получив путь - адрес папки с комиксом - функция перероет все подпапки
    и вернет список со словарями, состоящими из двух элементов -
    адреса htm-файла и адреса его папки с файлами.
    """
    list_htm_and_folder: list[tuple[Path, Path]] = []
    for directory, folders, files in comic.walk():
        htm_files = [
            Path(htm_file)
            for htm_file
            in files
            if '.htm' in Path(htm_file).suffix
        ]
        for htm_file in htm_files:
            name_folder = htm_file.stem + '_files'
            if name_folder in folders:
                list_htm_and_folder.append(
                    (
                        Path(directory, htm_file),
                        Path(directory, name_folder)
                    )
                )
    return list_htm_and_folder


def identify_site(example_soup: bs4.BeautifulSoup):
    if example_soup.link:
        link = str(example_soup.link.attrs['href'])
        files = [
            fl
            for fl
            in Path('site_and_selectors').iterdir()
            if (
                fl.is_file()
                and fl.suffix == '.json'
            )
        ]
        for fl in files:
            with open(fl, 'r', encoding='utf-8') as f:
                json_file: SiteSelectors = json.load(f)
            if link in json_file['name_site']:
                return json_file
    return False


def search_name_image(site: bs4.BeautifulSoup, scheme: SiteSelectors):
    images = site.select(scheme['selector'])
    list_images = [
        Path(
            str(image.attrs[scheme['tag']])
        ).name.partition(scheme['symbol'])[0]
        for image
        in images
    ]
    return list_images


def general_extract(
        method: Callable, files: list[str],
        source: Path, target: Path
):
    images_path = [
        source / i
        for i
        in files
        if (source / i).exists()
    ]
    if not len(files) == len(images_path):
        raise Exception
    target.mkdir(parents=True, exist_ok=True)
    method(images_path=images_path, target=target)


def orchestra(settings: Settings, comic: Path, method: Callable):
    technical_folder = [
        settings['original'],
        settings['editor'],
        settings['translate']
    ] + settings['other_folder']
    htm_files = search_htm_files(comic)
    for site_file, site_dir in htm_files:
        if site_file.parent == comic:
            # Файл сайта находится в папке комикса
            path_max_chapter = max(
                list_chapters(comic, technical_folder),
                key=key_max_chapters,
                default=Path('0')
            )
            number = str(Chapter(path_max_chapter).number + 1)
            chapter = Chapter(comic / number)
        else:
            # Файл сайта находится в подпапках
            count = 1
            while True:
                if site_file.parents[count] == comic:
                    break
                count += 1
            chapter = Chapter(site_file.parents[count - 1])
        chapter.create()

        # Идентификация сайта
        with open(site_file, "r", encoding="utf-8") as fl:
            example_soup = bs4.BeautifulSoup(
                fl.read(),
                'html.parser'
            )
        site_scheme = identify_site(example_soup)
        if not site_scheme:
            continue

        list_name_image = search_name_image(example_soup, site_scheme)
        general_extract(
            method=method,
            files=list_name_image,
            source=site_dir,
            target=chapter / settings['original']
        )
        if settings['delete']:
            send2trash.send2trash([site_file, site_dir])
        elif site_file.parent == comic:
            shutil.move(site_file, chapter)
            shutil.move(site_dir, chapter)
