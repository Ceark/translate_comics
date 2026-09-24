import json
import shutil
from pathlib import Path
from typing import Callable

import bs4
import send2trash

from constants import path_site_and_selectors
from custom_class.custom_class import Comic
from custom_typing.custom_typing import SiteSelectors


def search_htm_files(comic: Path) -> list[tuple[Path, Path]]:
    """Получить список кортежей, состоящих из адреса файла сайта
    и адреса его папки с файлами."""
    list_htm_and_folder: list[tuple[Path, Path]] = []
    for htm in comic.rglob('*.htm*'):
        if htm.is_file() and '.htm' in htm.suffix:
            folder = Path(htm.parent, htm.stem + '_files')
            if folder.is_dir():
                list_htm_and_folder.append((htm, folder))
    return list_htm_and_folder


def specify_target(
        htm: Path, htm_folder: Path, comic: Comic
) -> tuple[Path, Path]:
    """Разместить файл комикса и папку с его файлами в папке части."""
    if htm.parent == comic:
        new_chapter = comic.create_chapter()
        return (
            Path(shutil.move(htm, new_chapter)),
            Path(shutil.move(htm_folder, new_chapter))
        )
    elif len(htm.parts) - len(comic.parts) > 1:
        chapter = htm.parents[len(htm.parts) - len(comic.parts) - 2]
        return (
            Path(shutil.move(htm, chapter)),
            Path(shutil.move(htm_folder, chapter))
        )
    else:
        return (htm, htm_folder)


def identify_site(example_soup: bs4.BeautifulSoup):
    """Получить адрес сайт из тэга link.

    Функция берет из тэга link адрес сайта, берет json-файлы из папки
    'site_and_selectors', находящейся рядом, и сравнивает адрес с 'name_site'
    из json-файла.

    Если что-то пошло не так - нет тэга link или не совпали адрес и все
    'name_site' - возвращает False.
    """
    if example_soup.link:
        link = str(example_soup.link.attrs['href'])
        files = [
            fl
            for fl
            in path_site_and_selectors.glob('*.json')
            if fl.is_file()
        ]
        for path in files:
            with open(path, 'r', encoding='utf-8') as fl:
                json_file: SiteSelectors = json.load(fl)
                if json_file['name_site'] in link:
                    return json_file
    return False


def search_name_image(site: bs4.BeautifulSoup, scheme: SiteSelectors):
    """
    Поиск имен файлов изображений в соответствии с полученной схемой.
    """
    for selector in scheme['selectors']:
        images = site.select(selector)
        if images:
            list_images = [
                Path(
                    str(image.attrs[scheme['tag']])
                ).name.partition(scheme['symbol'])[0]
                for image
                in images
            ]
            return list_images
    return []


def validate_images(image_names: list[str], htm_folder: Path) -> list[Path]:
    images_path = [
        htm_folder / name
        for name
        in image_names
        if (htm_folder / name).exists()
    ]
    if len(image_names) == len(images_path):
        return images_path
    else:
        raise Exception


def orchestra(comic: Comic, method: Callable, delete: bool, target: str):
    """Управление извлечением изображений комикса.

    comic - папка комикса;
    method - функция экстрации;
    delete - удалять ли данные сайта;
    target - имя папки, в которую производится экстрация.
    """
    htm_files = search_htm_files(comic)
    for htm, folder in htm_files:
        htm, folder = specify_target(htm, folder, comic)
        with open(htm, "r", encoding="utf-8") as fl:
            example_soup = bs4.BeautifulSoup(fl.read(), 'html.parser')
        site_scheme = identify_site(example_soup)
        if not site_scheme:
            continue
        image_names = search_name_image(example_soup, site_scheme)
        image_paths = validate_images(image_names, folder)
        method(images=image_paths, target=folder.parent / target)
        if delete:
            send2trash.send2trash([htm, folder])
