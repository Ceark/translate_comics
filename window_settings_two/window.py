import tkinter as tk
from functools import partial

from constants import strings
from custom.typing import Settings, SettingsVar

from .functions import button_choose, update_settings
from .widgets import (tk_button, tk_checkbutton, tk_combobox, tk_entry,
                      tk_frame, tk_labels, tk_spinbox, window_settings)


def open_settings(root: tk.Tk, settings: Settings):
    variable: SettingsVar = {
        'base_dir': tk.StringVar(value=str(settings['base_dir'])),
        'original': tk.StringVar(value=settings['original']),
        'editor': tk.StringVar(value=settings['editor']),
        'translate': tk.StringVar(value=settings['translate']),
        'other_folder': tk.StringVar(
            value=', '.join(settings['other_folder'])
        ),
        'ignore_folder': tk.StringVar(
            value=', '.join(settings['ignore_folder'])
        ),
        'delete': tk.BooleanVar(value=settings['delete']),
        'length_number': tk.IntVar(value=settings['length_number']),
        'move_images': {
            'where': tk.StringVar(value=settings['move_images']['where']),
            'to': tk.StringVar(value=settings['move_images']['to']),
            'suffix': tk.StringVar(value=settings['move_images']['suffix'])
        }
    }
    window = window_settings(root, 'Настройки', '300x300')
    quantity_row = len(strings) + 1
    mainframe = tk_frame(window, column=2, row=quantity_row)
    iterator = (i for i in range(quantity_row))
    # Строки сбоку
    tk_labels(
        mainframe, strings,
        **{'column': 0, 'padx': '5', 'sticky': 'w'}
    )
    # Поле адреса главной папки; двойное нажатие - выбор адреса папки
    tk_entry(
        mainframe, variable['base_dir'],
        **{'column': 1, 'row': next(iterator)}
    ).bind('<Double-1>', lambda x: button_choose(variable['base_dir']))
    # Поле папки оригинала
    tk_entry(
        mainframe, variable['original'],
        **{'column': 1, 'row': next(iterator)}
    )
    # Поле папки с изменяемыми файлами
    tk_entry(
        mainframe, variable['editor'],
        **{'column': 1, 'row': next(iterator)}
    )
    # Поле папки перевода
    tk_entry(
        mainframe, variable['translate'],
        **{'column': 1, 'row': next(iterator)}
    )
    # Поле для других папок
    tk_entry(
        mainframe, variable['other_folder'],
        **{'column': 1, 'row': next(iterator)}
    )
    # Поле игнорируемых папок
    tk_entry(
        mainframe, variable['ignore_folder'],
        **{'column': 1, 'row': next(iterator)}
    )
    # Флажок удаления
    tk_checkbutton(
        mainframe, variable['delete'],
        **{'column': 1, 'row': next(iterator)}
    )
    # Спин-бокс длины числа
    tk_spinbox(
        mainframe, variable['length_number'],
        **{'column': 1, 'row': next(iterator)}
    )
    # Перемещение файлов
    folders_settings = [
        settings['original'],
        settings['editor'],
        settings['translate']
    ] + settings['other_folder']
    # Откуда перемещать файлы
    tk_combobox(
        mainframe, variable['move_images']['where'], folders_settings,
        **{'column': 1, 'row': next(iterator)}
    )
    # Куда перемещать файлы
    tk_combobox(
        mainframe, variable['move_images']['to'], folders_settings,
        **{'column': 1, 'row': next(iterator)}
    )
    # Суффикс
    tk_entry(
        mainframe, variable['move_images']['suffix'],
        **{'column': 1, 'row': next(iterator)}
    )
    # Кнопка сохранения
    command_save = partial(update_settings, settings, variable)
    tk_button(
        mainframe, 'Сохранить',
        **{'column': 1, 'row': next(iterator)}
    )['command'] = command_save
    # Запуск
    window.mainloop()


# def open_settings(
#         root_window: tk.Tk,
#         settings: Settings,
#         strings: tuple,
#         widgets_main: WidgetsMain,
#         widgets_main_var: WidgetsMainVar
# ):
#     window = window_settings(root_window, 'Settings', '300x300+550+220', 3, 8)
#     tk_labels(window, strings, 0, 5)
#     widgets_var = SettingsVar(
#         base_dir=first_row(window, 1, 0, str(settings['base_dir'])),
#         original=folder_name(window, 1, 1, settings['original']),
#         editor=folder_name(window, 1, 2, settings['editor']),
#         translate=folder_name(window, 1, 3, settings['translate']),
#         other_folder=folder_name(
#             window, 1, 4, ', '.join(settings['other_folder'])
#         ),
#         delete=tk_checkbutton(window, 1, 5, settings['delete']),
#         length_number=tk_spinbox(window, 1, 6, settings['length_number'])
#     )
#     save_button(
#          window=window,
#          column=0, row=7,
#          settings=settings,
#          widgets_var=widgets_var, widgets_main=widgets_main,
#          widgets_main_var=widgets_main_var
#     )
