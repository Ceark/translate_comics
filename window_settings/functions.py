import tkinter as tk
from pathlib import Path
from tkinter import filedialog

from constants import path_settings
from custom.typing import MoveImagesSettings, Settings, SettingsVar
from manage_settings.save_settings import save_dict_settings


def button_choose(string_var: tk.StringVar):
    """
    Функция, которая спрашивает у пользователя каталог и вставляет полученное
    значение в переменную StrVar.
    """
    path = filedialog.askdirectory()
    if path == '':
        return None
    if not path == '.':
        string_var.set(path)


def update_settings(
        settings: Settings,
        variable: SettingsVar
):
    """
    Функция формирует новый словарь настроек, обновляет текущие настройки,
    сохраняет новый словарь настроек в файл, и обновляет виджеты главного окна.
    """
    new_settings = Settings(
        base_dir=Path(variable['base_dir'].get()),
        original=variable['original'].get(),
        editor=variable['editor'].get(),
        translate=variable['translate'].get(),
        other_folder=variable['other_folder'].get().split(', '),
        ignore_folder=variable['ignore_folder'].get().split(', '),
        delete=variable['delete'].get(),
        length_number=variable['length_number'].get(),
        move_images=MoveImagesSettings(
            where=variable['move_images']['where'].get(),
            to=variable['move_images']['to'].get(),
            suffix=variable['move_images']['suffix'].get(),
        )
    )
    settings.update(new_settings)
    save_dict_settings(path=path_settings, dct=new_settings)
