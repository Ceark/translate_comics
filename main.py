import json
import tkinter as tk
from functools import partial
from pathlib import Path
from tkinter import ttk

from custom_typing import PythonSettings
from window_settings import open_settings


def tk_window(title, geometry, column, row):
    window = tk.Tk()
    window.title(title)
    window.geometry(geometry)
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


address_settings = Path('settings.json')
try:
    with open(address_settings, 'r', encoding='utf-8') as file:
        settings: PythonSettings = json.load(file)
        if not Path(settings['base_dir']).exists():
            raise ValueError
except (FileNotFoundError, ValueError):
    settings = {
        'base_dir': str(Path().cwd()),
        'original': 'Original',
        'editor': 'Редактор',
        'translate': 'Перевод',
        'other_folder': 'Текст',
        'delete': False,
        'length_number': 2
    }

main_window = tk_window('tr_comic', '200x200+500+190', 2, 4)


# Строка выбор комикса
def row_combobox(window: tk.Tk, column, row, settings: PythonSettings):
    def update_combobox(combobox: ttk.Combobox, str_var=tk.StringVar):
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

    upadate = partial(update_combobox, combobox)
    upadate()

    button_update = tk.Button(
        window,
        text='\u27F3',
        command=upadate
    )
    button_update.grid(
        column=column, row=row, columnspan=2, sticky='w', padx=10
    )
    return str_var


base_dir = row_combobox(main_window, 0, 0, settings)
# Первый столбец
# Экстракция


def command_extraction():
    pass


button_extraction = tk.Button(
    main_window, text='Экстракция', command=command_extraction
)
# Перемещение
# Ярлыки

# Второй столбец
# Создание комикса
# Добавление частей

# Окно настроек
strings = (
    'Комиксы',
    'Оригинал',
    'Редактор',
    'Перевод',
    'Доп. папки',
    'Удалить файлы',
    'Длина числа',
)
command_settings = partial(
    open_settings, main_window, address_settings, settings, strings
)
button_open_settings = tk.Button(
    main_window, text='Settings', command=command_settings
)
button_open_settings.grid(column=1, row=3)

# Запуск
main_window.mainloop()
