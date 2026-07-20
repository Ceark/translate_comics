import tkinter as tk
from functools import partial
from pathlib import Path
from tkinter import ttk
from typing import Callable

from custom_typing import PythonSettings


def tk_window(title: str, geometry: str, column: int, row: int):
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
        window: tk.Tk, column: int, row: int,
        settings: PythonSettings
):
    def update_combobox(combobox: ttk.Combobox, str_var=tk.StringVar):
        str_var.set(value='')
        combobox['values'] = [
            value.name
            for value
            in Path(settings['base_dir']).iterdir()
            if value.is_dir()
        ]

    str_var = tk.StringVar()
    combobox = ttk.Combobox(window, textvariable=str_var, state='readonly')
    combobox.grid(
        column=column, row=row, columnspan=window.grid_size()[0],
        sticky='e', padx=10
    )

    update = partial(update_combobox, combobox, str_var)
    update()

    button_update = tk.Button(window, text='\u27F3', command=update)
    button_update.grid(
        column=column, row=row, columnspan=2, sticky='w', padx=10
    )
    return str_var


def button_settings(
        window: tk.Tk, text: str, command: Callable,
        column: int, row: int
):
    button = tk.Button(
        window, text=text, command=command
    )
    button.grid(column=column, row=row)
