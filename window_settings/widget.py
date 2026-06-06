import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog


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
    return window


def tk_labels(window, strings, column):
    """
    Расположить строки в столбце, одна строка на строку.
    """
    labels = [
        tk.Label(window, text=value)
        for value
        in strings
    ]
    for index, label in enumerate(labels):
        label.grid(
            column=column,
            row=index,
            padx=20,
            sticky='w'
        )
    return labels


def first_row(window, column, row, value):
    """
    Строка ввода для адреса папки и кнопка выбора папки.
    """
    string_var = tk.StringVar(value=value)
    entry = tk.Entry(window, textvariable=string_var)
    entry.grid(column=column, row=row, sticky='w')

    def button_choose():
        path = filedialog.askdirectory()
        if path == '.':
            return None
        string_var.set(Path(path))

    button = tk.Button(window, text='Выбор...', command=button_choose)
    button.grid(column=column + 1, row=row)
    return string_var


def folder_name(window, column, row, value):
    """
    Поле ввода для имен папок.
    """
    string_var = tk.StringVar(value=value)
    entry = tk.Entry(window, textvariable=string_var, width=28)
    entry.grid(column=column, columnspan=2, row=row, sticky='w')
    return string_var


def tk_checkbutton(window, column, row, value: bool):
    """
    Переменная-флажок, возвращающая булевы значения.
    """
    bool_var = tk.BooleanVar(value=value)
    checkbutton = tk.Checkbutton(
        window,
        variable=bool_var,
        offvalue=False,
        onvalue=True
    )
    checkbutton.grid(column=column, row=row, sticky='w', padx=5)
    return bool_var


def tk_spinbox(window, column, row, value: int):
    """
    Счётчик от одного до пяти.
    """
    int_var = tk.IntVar(value=value)
    spinbox = tk.Spinbox(window, from_=1, to=5, textvariable=int_var)
    spinbox.grid(column=column, row=row)
    return int_var


def save_button(window, column, row, widgets):
    """Кнопка сохранения файла настроек."""
    def create_data_json():
        """
        Получение из виджетов введёных данных,
        оформление полученного адреса для 'base_dir'
        и создание из строки, полученной из 'other_folder', списка.
        """
        save_data = {
            key: widgets[key].get()
            for key
            in widgets
        }
        save_data['base_dir'] = str(Path(save_data['base_dir']))
        save_data['other_folder'] = [
            string.strip()
            for string
            in save_data['other_folder'].split(',')
        ]
        return save_data

    def save_json_file():
        """Сохранить файл настроек рядом с исполняемой программой."""
        with open(
            Path('.', 'settings.json'),
            'w', encoding="utf-8"
        ) as file:
            json.dump(
                create_data_json(),
                file,
                indent=4,
                ensure_ascii=False
            )

    button = tk.Button(window, text='Сохранить', command=save_json_file)
    button.grid(column=column, row=row, columnspan=3)
