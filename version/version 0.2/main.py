from pathlib import Path
from shutil import copy

from bs4 import BeautifulSoup


def extraction_image(site_file: Path, action):
    """
    Функция для обработки отедльного файла сайта.
    """
    parent = site_file.parent
    site_dir = parent / (site_file.stem + '_files')
    # Открытие файла
    try:
        with open(site_file, "r", encoding="utf-8") as file:
            example_soup = BeautifulSoup(
                file.read(),
                'html.parser'
            )
    except FileNotFoundError:
        return f'Файл {site_file} не существует.'
    # Формирование списка файлов изображений
    selector = 'img[class="content__img js-lazy"]'
    elems = example_soup.select(selector)
    image_files = [
        Path(Path(value.attrs['src']).name) for value in elems
    ]
    # Экстракция
    for index, file in enumerate(image_files, 1):
        try:
            copy(
                site_dir / file,
                parent / (f'{index}' + f'{file.suffix}')
            )
        except FileNotFoundError:
            if not site_dir.exists():
                return f'Папка с файлами сайта - {site_dir.name} - не найдена.'
            elif not (site_dir / file).exists():
                return (
                    f'Изображение {(site_dir / file).name} не найдено.\n'
                    + 'Пожалуйста, загрузите файл сайта заново.'
                )
        except Exception:
            return 'Неизвестная ошибка, связанная с копированием изображений.'
    return 'Копирование изображений завершено.'


value = Path(input('Введите путь к html-файлу: '))
print(extraction_image(value))
input('Нажмите Enter для завершения работы.')
