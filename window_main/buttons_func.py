import tkinter as tk
from pathlib import Path
from shutil import move

from send2trash import send2trash

from custom.klass import Comic
from extract_image.functions import copy_images, unite
from extract_image.logic import orchestra

from .subfunctions import shortcut


def command_extract(
        base_dir: Path, delete: bool, original: str,
        comic_variable: tk.StringVar, regime_variable: tk.StringVar
):
    """Функция для кнопки экстракции."""
    func_extract = {
        'copy': copy_images,
        'union': unite
    }
    func = func_extract[regime_variable.get()]
    comic = Comic(base_dir / comic_variable.get())
    orchestra(comic, func, delete, original)


def command_add_chapter(
        base_dir: Path, comic_variable: tk.StringVar,
        quantity_variable: tk.IntVar
):
    """Функция для кнопки добавления части."""
    comic = Comic(base_dir / comic_variable.get())
    comic.create_chapters(quantity_variable.get())


def command_move_files(
        base_dir: Path, comic_variable: tk.StringVar,
        where_from_variable: tk.StringVar, where_to_variable: tk.StringVar,
        suffix_variable: tk.StringVar,
):
    """
    Функция для кнопки перемещения файлов.

    Если в папке уже есть файл с таким же названием, он будет перемещен
    в корзину.
    """
    where_from = where_from_variable.get()
    where_to = where_to_variable.get()
    if not where_from == where_to:
        comic = Comic(base_dir / comic_variable.get())
        suffix = suffix_variable.get()
        for chapter in comic.list_chapters():
            for fl in (comic / chapter / where_from).glob(suffix):
                dst = (comic / chapter / where_to)
                dst.mkdir(exist_ok=True)
                if (dst / fl.name).exists():
                    send2trash(dst / fl.name)
                move(fl, dst)


def command_shortcut(
        base_dir: Path, comic_variable: tk.StringVar,
        folders_variable: tk.StringVar
):
    """Функция для кнопки создания ярлыков.

    Если в папке есть файлы с одинаковыми именами и разными суффиксами,
    то ярлыком станет только последний."""
    comic = Comic(base_dir / comic_variable.get())
    shortcut_folder = comic / folders_variable.get()
    shortcut_folder.mkdir(exist_ok=True)
    for chapter in comic.list_chapters():
        chapter_folder = chapter / folders_variable.get()
        chapter_folder.mkdir(exist_ok=True)
        for obj in chapter_folder.iterdir():
            shortcut_name = chapter.rjust_number + '_' + obj.stem + '.lnk'
            shortcut_path = shortcut_folder / shortcut_name
            shortcut(
                shortcut_path=str(shortcut_path),
                target_path=str(obj)
            )
