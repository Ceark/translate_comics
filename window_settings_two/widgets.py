import tkinter as tk
from tkinter import ttk


def window_settings(root: tk.Tk, title: str, geometry: str):
    """Создание дочернего окна настроек."""
    window = tk.Toplevel(root)
    window.title(title)
    window.geometry(geometry)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    return window


def tk_frame(root: tk.Tk, column: int, row: int):
    """Создание фрэйма."""
    frame = ttk.Frame(root)
    frame.grid(column=0, row=0, sticky='nsew')
    for i in range(column):
        frame.columnconfigure(i, weight=1)
    for i in range(row):
        frame.rowconfigure(i, weight=1)
    return frame


def tk_labels(root: tk.Frame, strings: list[str], **kwargs):
    """Надписи в левой части окна."""
    labels = [
        tk.Label(root, text=string)
        for string
        in strings
    ]
    for index, label in enumerate(labels):
        label.grid(row=index, **kwargs)


def tk_entry(root: tk.Frame, variable: tk.StringVar, **kwargs):
    """Поле для ввода имен папок."""
    entry = tk.Entry(root, textvariable=variable)
    entry.grid(**kwargs)
    return entry


def tk_checkbutton(root: tk.Frame, variable: tk.BooleanVar, **kwargs):
    """Переменная-флажок, возвращающая булевы значения."""
    checkbutton = tk.Checkbutton(
        root, offvalue=False, onvalue=True, variable=variable
    )
    checkbutton.grid(**kwargs)


def tk_spinbox(root: tk.Frame, variable: tk.IntVar, **kwargs):
    """Спин-бокс от одного до пяти."""
    spinbox = tk.Spinbox(root, from_=1, to=5, textvariable=variable, width=5)
    spinbox.grid(**kwargs)


def tk_combobox(
        root: tk.Frame, variable: tk.StringVar, values: list[str], **kwargs
):
    """Комбо-бокс."""
    commbobox = ttk.Combobox(root, textvariable=variable, state='readonly')
    commbobox['values'] = values
    commbobox.grid(**kwargs)


def tk_button(root: tk.Frame, text: str, **kwargs):
    button = ttk.Button(root, text=text)
    button.grid(**kwargs)
    return button

# def save_button(
#         window: tk.Toplevel,
#         column: int, row: int,
#         settings: Settings,
#         widgets_var: SettingsVar,
#         widgets_main: WidgetsMain,
#         widgets_main_var: WidgetsMainVar
# ):
#     """Кнопка сохранения файла настроек."""
#     command = partial(
#         update_settings, settings, widgets_var, widgets_main,
#         widgets_main_var
#     )
#     button = tk.Button(window, text='Сохранить', command=command)
#     button.grid(column=column, row=row, columnspan=window.grid_size()[0])
