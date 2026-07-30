import tkinter as tk
from functools import partial
from pathlib import Path
from tkinter import filedialog, ttk

from constants import path_settings
from custom_typing.custom_typing import Settings, WidgetsVar, WidgetsMain
from manage_settings.save_settings import save_dict_settings
from .functions import update_settings


def window_settings(
        root_window: tk.Tk,
        title: str, geometry: str,
        column: int, row: int
):
    """
    Создание дочернего окна настроек.
    """
    window = tk.Toplevel(root_window)
    window.title(title)
    window.geometry(geometry)
    for i in range(column):
        window.columnconfigure(index=i, weight=1)
    for i in range(row):
        window.rowconfigure(index=i, weight=1)
    return window


def tk_labels(
        window: tk.Toplevel,
        strings: tuple[str],
        column: int,
        padx: int
):
    """
    Заполнит столбец строками.
    """
    labels = [
        tk.Label(window, text=string)
        for string
        in strings
    ]
    for index, label in enumerate(labels):
        label.grid(
            column=column,
            row=index,
            padx=padx,
            sticky='w'
        )


def button_choose(string_var: tk.StringVar):
    path = filedialog.askdirectory()
    if not path == '.':
        string_var.set(path)


def first_row(
        window: tk.Toplevel,
        column: int, row: int,
        default: str
):
    """
    Строка ввода для адреса папки и кнопка выбора папки.
    """
    string_var = tk.StringVar(value=default)
    entry = tk.Entry(window, textvariable=string_var)
    entry.grid(column=column, row=row, sticky='w', padx=10)
    function_button = partial(button_choose, string_var)
    button = tk.Button(window, text='Выбор', command=function_button)
    button.grid(column=column + 1, row=row, padx=5, sticky='ew')
    return string_var


def folder_name(
        window: tk.Toplevel,
        column: int, row: int,
        default: str
):
    """
    Поле ввода для имен папок.
    """
    string_var = tk.StringVar(value=default)
    entry = tk.Entry(window, textvariable=string_var)
    entry.grid(column=column, columnspan=2, row=row, sticky='we', padx=10)
    return string_var


def tk_checkbutton(
        window: tk.Toplevel,
        column: int, row: int,
        default: bool
):
    """
    Переменная-флажок, возвращающая булевы значения.
    """
    bool_var = tk.BooleanVar(value=default)
    checkbutton = tk.Checkbutton(
        window,
        variable=bool_var,
        offvalue=False,
        onvalue=True
    )
    checkbutton.grid(column=column, row=row, sticky='w', padx=5)
    return bool_var


def tk_spinbox(
        window: tk.Toplevel,
        column: int, row: int,
        default: int
):
    """
    Счётчик от одного до пяти.
    """
    int_var = tk.IntVar(value=default)
    spinbox = tk.Spinbox(
        window, from_=1, to=5, textvariable=int_var, width=4
    )
    spinbox.grid(column=column, row=row, sticky='w', padx=10)
    return int_var


def save_button(
        window: tk.Toplevel,
        column: int, row: int,
        settings: Settings,
        widgets_var: WidgetsVar,
        widgets_main: WidgetsMain
):
    """Кнопка сохранения файла настроек."""
    command = partial(update_settings, settings, widgets_var, widgets_main)
    # command = partial(save_dict_settings, path_settings, settings, widgets_var)
    button = tk.Button(window, text='Сохранить', command=command)
    button.grid(column=column, row=row, columnspan=window.grid_size()[0])
