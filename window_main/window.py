import tkinter as tk
from functools import partial

from custom.typing import DictVariable, Settings

from .buttons_func import (command_add_chapter, command_extract,
                           command_move_files, command_shortcut)
from .widgets import (add_chapters, comics_list, create_shortcut, extraction,
                      move_images, tk_frame, tk_separators, tk_window)


def open_main(settings: Settings):
    window = tk_window('tr_comic', '355x300')
    mainframe = tk_frame(window, column=2, row=3)
    tk_separators(mainframe, vertical=1, horizontal=2)

    variable: DictVariable = {
        'comic': tk.StringVar(),
        'regime': tk.StringVar(value='copy'),
        'quantity': tk.IntVar(value=1),
        'where_from': tk.StringVar(value=settings['editor']),
        'where_to': tk.StringVar(value=settings['translate']),
        'suffix': tk.StringVar(value='*.'),
        'folders': tk.StringVar(value=settings['original'])
    }

    # Выпадающий список комиксов
    combobox_list_comics = comics_list(
        mainframe,
        variable['comic'],
        settings['base_dir'],
        **{'column': 0, 'row': 0, 'columnspan': 2}
    )

    # Экстракция
    button_extract = extraction(
        mainframe, variable['regime'],
        **{'column': 0, 'row': 1, 'padx': 5, 'pady': 5}
    )
    functon_extract = partial(
        command_extract,
        base_dir=settings['base_dir'],
        delete=settings['delete'],
        original=settings['original'],
        comic_variable=variable['comic'],
        regime_variable=variable['regime']
    )
    button_extract['command'] = functon_extract

    # Переместить изображения
    values = [
        settings['original'],
        settings['editor'],
        settings['translate']
    ] + settings['other_folder']
    button_move_images = move_images(
        mainframe,
        variable['where_from'],
        variable['where_to'],
        variable['suffix'],
        values,
        **{'column': 1, 'row': 1, 'padx': 5, 'pady': 5}
    )
    function_move_files = partial(
        command_move_files,
        base_dir=settings['base_dir'],
        comic_variable=variable['comic'],
        where_from_variable=variable['where_from'],
        where_to_variable=variable['where_to'],
        suffix_variable=variable['suffix']
    )
    button_move_images['command'] = function_move_files

    # Добавить часть
    button_chapters = add_chapters(
        mainframe, variable['quantity'],
        **{'column': 0, 'row': 2, 'padx': 5, 'pady': 5}
    )
    function_add_chapters = partial(
        command_add_chapter,
        base_dir=settings['base_dir'],
        comic_variable=variable['comic'],
        quantity_variable=variable['quantity']
    )
    button_chapters['command'] = function_add_chapters

    # Создать ярлыки
    button_shortcut = create_shortcut(
        mainframe,
        variable['folders'],
        values,
        **{'column': 1, 'row': 2, 'pady': 5}
    )
    function_shortcut = partial(
        command_shortcut,
        settings['base_dir'],
        variable['comic'],
        variable['folders']
    )
    button_shortcut['command'] = function_shortcut

    # Запуск окна
    window.mainloop()
