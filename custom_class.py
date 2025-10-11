import os
import shutil
from pathlib import Path

import bs4
import pyinputplus as pyip
import send2trash
from PIL import Image

from extract_env import DIR_CHAPTER, DIR_COMIC, LENGTH_NUMBER, DELETE

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
                (self.path / long_number / directory).mkdir(parents=True)

    def extract_image(self, method):
        chapter_error: list[str] = []
        site_file_none: list[str] = []
        link_none: list[str] = []
        not_flag: list[str] = []
        not_image: list[str] = []

        for chapter in self.list_chapters():
            path_chapter: Path = (
                self.path / chapter / self.dir_chapter['original']
            )

            # Поиск файла сайта и папки с содержимым в папке Original
            if path_chapter.exists():
                site_dir, site_file = False, False
                for file in [
                    value for value in path_chapter.iterdir()
                    if value.is_file()
                    and '.htm' in value.suffix
                ]:
                    if (path_chapter / (file.stem + '_files')).exists():
                        site_dir = path_chapter / (file.stem + '_files')
                        site_file = file
                        break
                if not (site_dir and site_file):
                    site_file_none.append(chapter)
                    continue
            else:
                chapter_error.append(chapter)
                continue

            # Открытие файла
            with open(site_file, "r", encoding="utf-8") as file:
                example_soup = bs4.BeautifulSoup(
                    file.read(),
                    'html.parser'
                )

            # Определить сайт
            if example_soup.link is None:
                link_none.append(chapter)
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
                not_flag.append(chapter)
                continue

            # Формирование списка файлов изображений
            elems = example_soup.select(selector)
            image_names = [
                Path(value.attrs['src']).name for value in elems
            ]
            check_image = [
                Path(site_dir / file).exists() for file in image_names
            ]
            if False in check_image:
                not_image.append(chapter)
                continue

            # Экстракция
            if method == 'Извлечь':
                for index, file in enumerate(image_names, 1):
                    suffix = Path(file).suffix
                    shutil.move(
                        site_dir / file,
                        path_chapter / (f'{index}' + suffix)
                    )
            elif method == 'Соединить':
                width, height = 0, 0
                coordinates = [(width, height)]
                # Получить кортежи координат
                for file in image_names:
                    with Image.open(site_dir / file) as img:
                        height += img.height
                        coordinates.append((width, height))
                # Получить ширину изображения
                with Image.open(site_dir / file) as img:
                    width = img.width
                # Создание единого изображения
                with Image.new('RGB', (width, height)) as new_img:
                    for index, file in enumerate(image_names):
                        with Image.open(site_dir / file) as img:
                            copy_img = img.copy()
                            new_img.paste(copy_img, coordinates[index])
                            copy_img.close()
                    new_img.save(path_chapter / 'Union.png')

            # Удаление файлов
            if DELETE:
                send2trash.send2trash([site_dir, site_file])

        if chapter_error:
            print(
                f'В главах {", ".join(chapter_error)} отсутсвует',
                f'папка {self.dir_chapter["original"]}.'
            )
        if site_file_none:
            print(
                f'В главах {", ".join(site_file_none)} отсутсвует файл сайта.'
            )
        if link_none:
            print(
                f'В главах {", ".join(link_none)} файл сайта повреждён,',
                'отсутсвует тэг <link>.'
            )
        if not_flag:
            print(
                f'Для глав {", ".join(not_flag)} отсутсвует алгоритм',
                'обработки файлов. Доступна обработка для сайтов ',
                '"Tapas" и "WebToon".'
            )
        if not_image:
            print(
                f'В главах {", ".join(not_image)} отсутсвуют изображения',
                'указанные в файле сайта. Попробуйте загрузить сайт заново.'
            )


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
            method = pyip.inputMenu(
                choices=[
                    'Извлечь',
                    'Соединить'
                ],
                prompt='Что делать с изображениями:\n',
                numbered=True
            )
            comic.extract_image(method)
            return 'Процесс завершен.'
        return CANCEL
