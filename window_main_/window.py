import tkinter as tk
from functools import partial
from pathlib import Path

from constants import strings
from custom_typing_.custom_typing import Settings
from window_settings.window import open_settings

from .widgets import button_settings, row_combobox, tk_window


def open_main(
    settings: Settings,
    path_settings: Path
):
    window = tk_window('tr_comic', '200x320+500+190', 2, 4)
    dif_var = {
        'row_combobox': tk.StringVar()
    }
    widgets_one = {
        'row_combobox': row_combobox(
            window=window, settings=settings,
            column=0, row=0,
            str_var=dif_var['row_combobox']
        ),
    }
    widgets_two = {
        'settings': button_settings(
            window=window, settings=settings,
            column=1, row=3,
            text='Настройки', strings=strings,
            widgets_main=widgets_one
        )
    }
    # base_dir = row_combobox(window, 0, 0, settings)
    # strings = (
    #     'Комиксы',
    #     'Оригинал',
    #     'Редактор',
    #     'Перевод',
    #     'Доп. папки',
    #     'Удалить файлы',
    #     'Длина числа',
    # )
    # command_settings = partial(
    #     open_settings, window, path_settings, settings, strings
    # )
    # button_settings(
    #     window, 'Настройки', command_settings,
    #     column=1, row=3
    # )

    window.mainloop()
