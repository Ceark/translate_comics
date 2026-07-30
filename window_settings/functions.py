import tkinter as tk
from functools import partial
from pathlib import Path
from tkinter import filedialog, ttk

from constants import path_settings
from custom_typing.custom_typing import (Settings, WidgetsMain, WidgetsMainVar,
                                         SettingsVar)
from manage_settings.save_settings import save_dict_settings


def button_choose(string_var: tk.StringVar):
    """
    Функция, которая спрашивает у пользователя каталог и вставляет полученное
    значение в переменную StrVar.
    """
    path = filedialog.askdirectory()
    if not path == '.':
        string_var.set(path)


def update_settings(
        settings: Settings,
        widgets_var: SettingsVar,
        widgets_main: WidgetsMain,
        widgets_main_var: WidgetsMainVar
):
    """
    Функция формирует новый словарь настроек, обновляет текущие настройки,
    сохраняет новый словарь настроек в файл, и обновляет виджеты главного окна.
    """
    new_settings = Settings(
        base_dir=Path(widgets_var['base_dir'].get()),
        original=widgets_var['original'].get(),
        editor=widgets_var['editor'].get(),
        translate=widgets_var['translate'].get(),
        other_folder=widgets_var['other_folder'].get().split(', '),
        delete=widgets_var['delete'].get(),
        length_number=widgets_var['length_number'].get()
    )
    # Альтернативный вариант, но на него ругается MyPy
    """
    update_settings = {
        key: widgets[key].get()
        for key
        in (Settings.__required_keys__)
    }
    update_settings['base_dir'] = Path(widgets['base_dir'].get())
    update_settings['other_folder'] = widgets['other_folder'].get().split(', ')
    """
    settings.update(new_settings)
    save_dict_settings(path=path_settings, dct=new_settings)

    widgets_main['row_combobox']['values'] = [
        value.name
        for value
        in Path(settings['base_dir']).iterdir()
        if value.is_dir()
    ]
    if len(widgets_main['row_combobox']['values']):
        widgets_main_var['row_combobox'].set(
            widgets_main['row_combobox']['values'][0]
        )
