import tkinter as tk
from pathlib import Path
from tkinter import ttk

from function import qq


def tk_window(title, column, row):
    """
    Создание основы, рамки окна настроек.
    """
    window = tk.Tk()
    window.title(title)
    window.geometry("350x350")
    for index in range(column):  # столбцы
        window.columnconfigure(index=index, weight=1)
    for index in range(row):  # строки
        window.rowconfigure(index=index, weight=1)
    for i in range(column - 1):
        sep = ttk.Separator(window, orient='vertical')
        sep.grid(column=i, row=1, rowspan=row, sticky='ens')
    for i in range(row - 1):
        sep = ttk.Separator(window, orient='horizontal')
        sep.grid(row=i, columnspan=column, sticky='ews')
    return window


def row_combobox(window, column, row, path: Path):
    str_var = tk.StringVar()
    combobox = ttk.Combobox(window, textvariable=str_var, state='readonly')

    def update_combobox():
        combobox['values'] = [
            value.name
            for value
            in path.iterdir()
            if value.is_dir()
        ]

    update_combobox()
    combobox.grid(
        column=column, row=row, columnspan=2, sticky='e', padx=10
    )

    button_update = tk.Button(
        window,
        text='\u27F3',
        command=update_combobox
    )
    button_update.grid(
        column=column, row=row, columnspan=2, sticky='w', padx=10
    )
    pass


def field_create_comic(window, column, row):
    string_var = tk.StringVar()
    entry = tk.Entry(window, textvariable=string_var)
    entry.grid(column=column, row=row, sticky='n', pady=5)

    button = tk.Button(
        window,
        text='Создать комикс',
        command=lambda: qq(string_var)
    )
    button.grid(column=column, row=row, sticky='s', pady=5)

    return button


def field_create_chapters(window, column, row):
    int_var = tk.IntVar(value=1)
    entry = tk.Entry(window, textvariable=int_var)
    entry.grid(column=column, row=row, sticky='n', pady=5)

    button = tk.Button(
        window,
        text='Добавить часть',
        command=lambda: qq(int_var)
    )
    button.grid(column=column, row=row, sticky='s', pady=5)

    return button
