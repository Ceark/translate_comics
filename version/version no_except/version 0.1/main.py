from pathlib import Path
from shutil import copy

from bs4 import BeautifulSoup


def extraction_image(site_file: Path):
    """
    Функция для обработки отедльного файла сайта.
    """
    parent = site_file.parent
    site_dir = parent / (site_file.stem + '_files')
    # Открытие файла
    with open(site_file, "r", encoding="utf-8") as file:
        example_soup = BeautifulSoup(
            file.read(),
            'html.parser'
        )
    # Формирование списка файлов изображений
    selector = 'img[class="content__img js-lazy"]'
    elems = example_soup.select(selector)
    image_files = [
        Path(Path(value.attrs['src']).name) for value in elems
    ]
    # Экстракция
    for index, file in enumerate(image_files, 1):
        copy(
            site_dir / file,
            parent / (f'{index}' + f'{file.suffix}')
        )
    return 'Копирование изображений завершено.'


value = Path(input('Введите путь к html-файлу: '))
print(extraction_image(value))
input('Нажмите Enter для завершения работы.')
