import tkinter as tk
from functools import partial
from pathlib import Path
from tkinter import ttk

from custom_typing.custom_typing import Settings, WidgetsMain
from window_settings.window import open_settings


def tk_window(
        title: str, geometry: str,
        column: int, row: int
):
    """
    Создание главного окна.
    """
    window = tk.Tk()
    window.title(title)
    window.geometry(geometry)
    for index in range(column):
        window.columnconfigure(index=index, weight=1)
    for index in range(row):
        window.rowconfigure(index=index, weight=1)
    for i in range(column - 1):
        sep = ttk.Separator(window, orient='vertical')
        sep.grid(column=i, row=1, rowspan=row, sticky='ens')
    for i in range(row - 1):
        sep = ttk.Separator(window, orient='horizontal')
        sep.grid(row=i, columnspan=column, sticky='ews')
    return window


def row_combobox(
        window: tk.Tk, settings: Settings,
        column: int, row: int,
        str_var: tk.StringVar
):
    """
    Строка выбора комикса.
    """
    combobox = ttk.Combobox(window, textvariable=str_var, state='readonly')
    combobox['values'] = [
        value.name
        for value
        in Path(settings['base_dir']).iterdir()
        if value.is_dir()
    ]
    if len(combobox['values']):
        combobox.set(combobox['values'][0])
        str_var.set(combobox['values'][0])
    combobox.grid(
        column=column, row=row, columnspan=window.grid_size()[0],
    )
    return combobox


def button_settings(
        window: tk.Tk, settings: Settings,
        column: int, row: int,
        text: str, strings: tuple[str], widgets_main: WidgetsMain
):
    command = partial(
        open_settings,
        root_window=window,
        settings=settings,
        strings=strings,
        widgets_main=widgets_main
    )
    button = tk.Button(
        window, text=text, command=command
    )
    button.grid(column=column, row=row)
