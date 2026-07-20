import json
import tkinter as tk
from functools import partial
from pathlib import Path

from all_extract import extract, orchestra, unite
from custom_typing import PythonSettings
from widgets import row_combobox, tk_window
from window_settings.window import open_settings

# Настройки
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

main_window = tk_window('tr_comic', '200x320+500+190', 2, 4)
base_dir = row_combobox(main_window, 0, 0, settings)
# Первый столбец


# Экстракция
def extract_image(
        window: tk.Tk, column, row,
        settings: PythonSettings, comic: tk.StringVar
):
    def command_extraction(func_var: tk.StringVar, name_comic):
        dict_func = {
            'copy': extract,
            'glue': unite
        }
        comic_path = Path(settings['base_dir'], name_comic.get())
        orchestra(dict_func[func_var.get()], comic_path, settings)

    func_var = tk.StringVar(value='copy')
    rad_copy = tk.Radiobutton(
        window, text='Копировать', value='copy', variable=func_var
    )
    rad_copy.grid(
        column=column, row=row, sticky='w', padx=5
    )
    rad_glue = tk.Radiobutton(
        window, text='Склеить', value='glue', variable=func_var
    )
    rad_glue.grid(
        column=column, row=row, sticky='sw', pady=5, padx=5
    )

    extract_command = partial(
        command_extraction,
        func_var,
        comic
    )
    button_extraction = tk.Button(
        main_window, text='Извлечь', command=extract_command
    )
    button_extraction.grid(
        column=column, row=row, sticky='nw', pady=5, padx=5
    )


extract_image(main_window, 0, 1, settings, base_dir)
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
