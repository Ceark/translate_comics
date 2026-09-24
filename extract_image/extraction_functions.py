
import shutil
from pathlib import Path

from PIL import Image


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
            width = max(width, img.width)
            coordinates.append((0, height))
    with Image.new('RGB', (width, height)) as union:
        for index, image in enumerate(images):
            with Image.open(image) as img:
                union.paste(img, coordinates[index])
        union.save(target / 'Union.png')
