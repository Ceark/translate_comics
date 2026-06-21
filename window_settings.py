import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

from custom_typing import PythonSettings


def open_settings(
        root_window: tk.Tk,
        path_settings: Path,
        settings: PythonSettings,
        strings: tuple
):
    def window_settings(root_window, title, geometry, column, row):
        window = tk.Toplevel(root_window)
        window.title(title)
        window.geometry(geometry)
        for i in range(column):
            window.columnconfigure(index=i, weight=1)
        for i in range(row):
            window.rowconfigure(index=i, weight=1)
        return window

    def tk_labels(window, strings, column, padx):
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

    def first_row(window, column, row, default):
        """
        Строка ввода для адреса папки и кнопка выбора папки.
        """
        string_var = tk.StringVar(value=default)
        entry = tk.Entry(window, textvariable=string_var)
        entry.grid(column=column, row=row, sticky='w', padx=10)

        def button_choose():
            path = filedialog.askdirectory()
            if not path == '.':
                string_var.set(path)

        button = tk.Button(window, text='Выбор', command=button_choose)
        button.grid(column=column + 1, row=row, padx=5, sticky='ew')
        return string_var

    def folder_name(window, column, row, value):
        """
        Поле ввода для имен папок.
        """
        string_var = tk.StringVar(value=value)
        entry = tk.Entry(window, textvariable=string_var)
        entry.grid(column=column, columnspan=2, row=row, sticky='we', padx=10)
        return string_var

    def tk_checkbutton(window, column, row, default: bool):
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

    def tk_spinbox(window, column, row, default: int):
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
            column,
            row,
            widgets: dict[str, tk.StringVar],
            settings: PythonSettings
    ):
        """Кнопка сохранения файла настроек."""
        def save_json_file():
            """Сохранить файл настроек рядом с исполняемой программой."""
            with open(path_settings, 'w', encoding='utf-8') as file:
                save_data = {
                    key: widgets[key].get()
                    for key
                    in widgets
                }
                json.dump(
                    save_data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

        def update():
            for key in widgets:
                settings[key] = widgets[key].get()

        button = tk.Button(
            window, text='Сохранить',
            command=lambda: (save_json_file(), update())
        )
        button.grid(column=column, row=row, columnspan=window.grid_size()[0])

    window = window_settings(root_window, 'Settings', '300x300+550+220', 3, 8)
    tk_labels(window, strings, 0, 5)
    widgets = {
        'base_dir': first_row(window, 1, 0, settings['base_dir']),
        'original': folder_name(window, 1, 1, settings['original']),
        'editor': folder_name(window, 1, 2, settings['editor']),
        'translate': folder_name(window, 1, 3, settings['translate']),
        'other_folder': folder_name(window, 1, 4, settings['other_folder']),
        'delete': tk_checkbutton(window, 1, 5, settings['delete']),
        'length_number': tk_spinbox(window, 1, 6, settings['length_number'])
    }
    save_button(window, 0, 7, widgets, settings)
