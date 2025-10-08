import os
import shutil
from pathlib import Path

import bs4
import pyinputplus as pyip
import send2trash
from PIL import Image

from extract_env import DIR_CHAPTER, DIR_COMIC, LENGTH_NUMBER

CANCEL = 'Действие отменено.'


class Comic:
    dir_comic = DIR_COMIC
    dir_chapter = DIR_CHAPTER
    length_number = LENGTH_NUMBER

    def __init__(self, path: Path):
        self.path = path

    def self_create(self):
        """Создание папки комикса."""
        for directory in self.dir_comic.values():
            (self.path / directory).mkdir()

    def list_chapters(self):
        """
        Получить список папок комикса. Файлы и папки для ярлыков исключены.
        """
        chapters = [
            chapter for chapter in os.listdir(self.path)
            if (
                chapter not in self.dir_chapter.values()
                and (self.path / chapter).is_dir()
            )
        ]
        return chapters

    def add_chapter(self, repeat):
        """
        Добавить часть.
        Номер добавленной папки определяется сначала по значению 'max'.
        Сначала пытается найти число, если не удастся, то использует
        количество папок.
        """
        chapters = self.list_chapters()
        number = max(chapters) if chapters else '0'
        if not number.isdecimal():
            number = number.split('_')[0]
            if not number.isdecimal():
                number = len(chapters)
        number = int(number) + 1
        for number_chapter in range(number, number + repeat):
            long_number = str(number_chapter).rjust(self.length_number, '0')
            for directory in self.dir_chapter.values():
                (self.path / long_number / directory).mkdir()

    def extract_image(self):
        chapters = self.list_chapters()
        # Выбор способа экстракции
        method = pyip.inputMenu(
            choices=[
                'Извлечь',
                'Соединить'
            ],
            prompt='Что делать с изображениями:\n',
            numbered=True
        )
        # Обработка
        for chapter in chapters:
            print(f'Обработка папки "{chapter}".')
            path: Path = self.path / chapter / self.dir_chapter['original']

            # Поиск файла сайта и папки с содержимым в папке Original
            if path.exists():
                path_site_dir, path_site_file = False, False
                for file in [
                    value for value in path.iterdir()
                    if value.is_file()
                    and '.htm' in value.suffix
                ]:
                    if (path / (file.stem + '_files')).exists():
                        path_site_dir = path / (file.stem + '_files')
                        path_site_file = file
                        break
                if not (path_site_dir and path_site_file):
                    print(
                        f'В {path} нет *.htm-файла или папки с подходящим',
                        'названием.'
                    )
                    continue
            else:
                print(f'Путь {path} не существует. Переход к следующей части.')
                continue

            # Открытие файла
            with open(path_site_file, "r", encoding="utf-8") as file:
                example_soup = bs4.BeautifulSoup(
                    file.read(),
                    'html.parser'
                )

            # Сайт файла
            if example_soup.link is None:
                print(
                    'Не удалось найти тэг сайта.',
                    f'Попробуйте заново загрузить файл {path_site_file}.',
                    sep='\n'
                )
                continue
            link = example_soup.link.attrs['href']
            dict_site = {
                'tapas': (
                    'tapas' in link,
                    'img[class="content__img js-lazy"]'
                ),
                'webtoon': (
                    'webtoons' in link,
                    'img[class="_images"]'
                )
            }
            for value in dict_site:
                flag, selector = dict_site[value]
                if flag:
                    break
            if not flag:
                print(f'Нет инструкций для страницы {path_site_file}.')
                continue

            # Формирование списка файлов изображений
            elems = example_soup.select(selector)
            file_names = [
                Path(value.attrs['src']).name for value in elems
            ]
            test = [Path(path_site_dir / file).exists() for file in file_names]
            if False in test:
                print(
                    'Изображения, указанные в файле страницы, не найдены.',
                    'Попробуйте загрузить страницу заново. Пропуск.',
                    sep='\n'
                )

            # Экстракция
            if method == 'Извлечь':
                for index, file in enumerate(file_names, 1):
                    suffix = Path(file).suffix
                    if (path_site_dir / file).exists():
                        shutil.move(
                            path_site_dir / file,
                            path / (f'{index}' + suffix)
                        )

            elif method == 'Соединить':
                width, height = 0, 0
                coordinates = [(width, height)]
                # Получить кортежи координат
                for file_name in file_names:
                    with Image.open(path_site_dir / file_name) as img:
                        height += img.height
                        coordinates.append((width, height))
                # Получить ширину изображения
                with Image.open(path_site_dir / file_name) as img:
                    width = img.width
                # Создание единого изображения
                with Image.new('RGB', (width, height)) as new_img:
                    for index, file_name in enumerate(file_names):
                        with Image.open(path_site_dir / file_name) as img:
                            copy_img = img.copy()
                            new_img.paste(copy_img, coordinates[index])
                            copy_img.close()
                    new_img.save(path / 'Union.png')
            send2trash.send2trash([path_site_dir, path_site_file])


class MainFolder:
    def __init__(self, path: Path):
        self.path = path

    def create_comic(self):
        blockRegexes = [
            (
                '|'.join(os.listdir(self.path)),
                'Папка с таким названием уже существует.'
            ),
            (
                r'\.$',
                'Точка не может стоять в конце названия папки.'
            ),
            (
                r'[:<>"\/\\\|\?\*]',
                'В названии папки использованы недопустимые символы.'
            )
        ]
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
        return ''

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
            comic.extract_image()
            return 'Процесс завершен.'
        return CANCEL
