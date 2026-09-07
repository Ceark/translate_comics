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
    Функция копирует изображения в target и переименовывает их.

    Если в папке уже содержатся файлы с таким же именем, то они будут заменены.
    """
    for index, image in enumerate(images, 1):
        new_name = str(index) + image.suffix
        shutil.copy(
            image,
            target / new_name
        )


def unite(images: list[Path], target: Path):
    """
    Функция объединяет изображения в файл 'Union.png' (оригиналы не изменятся)
    и сохранит его в папку target.
    """
    width, height = 0, 0
    coordinates = [(0, height)]
    for image in images:
        with Image.open(image) as img:
            height += img.height
            coordinates.append((0, height))
    with Image.open(image) as img:
        width = img.width
    with Image.new('RGB', (width, height)) as union:
        for index, image in enumerate(images):
            with Image.open(image) as img:
                union.paste(img, coordinates[index])
        union.save(target / 'Union.png')


def list_chapters(comic: Path):
    """
    Получить список глав комикса.

    Глава комикса - любая папка, имя которой начинается с числа
    и не входит в список technical_folder.
    """
    chapters = [
        Chapter(chapter)
        for chapter
        in comic.iterdir()
        if Chapter(chapter).is_chapter()
    ]
    return chapters


def search_htm_files(comic: Path) -> list[tuple[Path, Path]]:
    """
    Функция возвращает список кортежей, состоящих из адреса htm-файла и адреса его папки с файлами.

    Получив путь - адрес папки с комиксом - функция перероет все подпапки
    и вернет список из кортежей, состоящими из двух элементов -
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
    """
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
    """
    Поиск имен файлов изображений в соответствии с полученной схемой.
    """
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
        method: Callable, image_names: list[str],
        htm_folder: Path, target: Path
):
    """
    Функция, объединяющая два метода экстрации.

    method - copy_images или unite.
    image_names - список имён файлов изображений
    """
    images_path = [
        htm_folder / i
        for i
        in image_names
        if (htm_folder / i).exists()
    ]
    if not len(image_names) == len(images_path):
        raise Exception
    target.mkdir(parents=True, exist_ok=True)
    method(images=images_path, target=target)


def orchestra(settings: Settings, comic: Path, method: Callable):
    htm_files = search_htm_files(comic)
    for site_file, site_dir in htm_files:
        # Если файл сайта находится в папке комикса
        if site_file.parents[0] == comic:
            max_number = max(
                list_chapters(comic),
                key=lambda i: Chapter(i).number
            ).number
            Chapter(comic, str(max_number)).create()
            target = Path(comic, str(max_number), settings['original'])
        # Если файл сайта находится где-то еще
        elif site_file.parents[1] == comic:  # В папке части
            target = site_file / settings['original']
        elif site_file.parents[2] == comic:  # В подпапке части
            target = site_file / settings['original']

        with open(site_file, "r", encoding="utf-8") as fl:
            example_soup = bs4.BeautifulSoup(
                fl.read(),
                'html.parser'
            )

        site_scheme = identify_site(example_soup)
        if not site_scheme:
            continue

        image_names = search_name_image(example_soup, site_scheme)

        general_extract(
            method=method,
            image_names=image_names,
            htm_folder=site_dir,
            target=target
        )

        if settings['delete']:
            send2trash.send2trash([site_file, site_dir])

if __name__ == '__main__':
    from pathlib import Path

    from constants import path_settings
    from custom_typing.custom_typing import Settings
    from manage_settings.load_settings import load_settings
    from window_main.window import open_main

    settings: Settings = load_settings(path_settings)

    orchestra(
        settings=settings,
        comic=Path(r"D:\MyDev\main\Stone's Coast"),
        method=copy_images
    )
