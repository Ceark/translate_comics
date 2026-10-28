import tkinter as tk
from pathlib import Path
from tkinter import ttk

from .subfunctions import list_comics_combobox_update
from .validation import check_num, check_suffix


def tk_window(title: str, geometry: str):
    """Создание главного окна."""
    window = tk.Tk()
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


def tk_separators(root: tk.Frame, vertical: int, horizontal: int):
    """Создание сепараторов."""
    for i in range(horizontal):
        sep = ttk.Separator(root, orient='horizontal')
        sep.grid(column=0, row=i, columnspan=2, sticky='swe')
    for i in range(vertical):
        sep = ttk.Separator(root, orient='vertical')
        sep.grid(column=i, row=1, rowspan=2, sticky='nse')


def comics_list(
        root: tk.Frame, comic_variable: tk.StringVar, base_dir: Path,
        **kwargs
):
    """Выпадающий список комиксов."""
    combobox = ttk.Combobox(
        root,
        textvariable=comic_variable,
        state='readonly'
    )
    combobox.grid(**kwargs)
    list_comics_combobox_update(combobox, base_dir)
    if combobox['values']:
        comic_variable.set(combobox['values'][0])
    combobox.bind(
        '<ButtonPress-1>',
        lambda x: list_comics_combobox_update(combobox, base_dir)
    )
    return combobox


def extraction(root: tk.Frame, regime_variable: tk.StringVar, **kwargs):
    """Кнопка экстракции и пара радиокнопок."""
    rad_copy = ttk.Radiobutton(
        root, text='Копировать', variable=regime_variable, value='copy'
    )
    rad_union = ttk.Radiobutton(
        root, text='Объединить', variable=regime_variable, value='union'
    )
    rad_copy.grid(**kwargs, sticky='nw')
    rad_union.grid(**kwargs, sticky='w')

    button_extract = ttk.Button(root, text='Извлечь')
    button_extract.grid(**kwargs, sticky='s')
    return button_extract


def add_chapters(root: tk.Frame, quantity_variable: tk.IntVar, **kwargs):
    """Кнопка добавления частей и поле ввода."""
    check_num_wrapper = (root.register(check_num), '%P')
    quantity_entry = tk.Entry(
        root, textvariable=quantity_variable,
        validate='key', validatecommand=check_num_wrapper,
        width=10, justify='center'
    )
    quantity_entry.grid(**kwargs, sticky='n')

    button_add_chapters = ttk.Button(
        root,
        text='Добавить часть'
    )
    button_add_chapters.grid(**kwargs, sticky='s')
    return button_add_chapters


def move_images(
        root: tk.Frame, where_from_variable: tk.StringVar,
        where_to_variable: tk.StringVar, suffix_variable: tk.StringVar,
        values: list[str], **kwargs
):
    """Кнопка перемещения изображений, два комбобокса выбора - откуда и куда,
    символ стрелки, поле ввода для суффикса перемещаемых файлов.
    """
    combobox_where_from = ttk.Combobox(
        root,
        textvariable=where_from_variable,
        state='readonly',
        width=10,
        values=values
    )
    combobox_where_to = ttk.Combobox(
        root,
        textvariable=where_to_variable,
        state='readonly',
        width=10,
        values=values
    )
    combobox_where_from.grid(**kwargs, sticky='nw')
    combobox_where_to.grid(**kwargs, sticky='ne')

    symbol_arrow = tk.Label(root, text='\u279d')
    symbol_arrow.grid(**kwargs, sticky='n')

    check_suffix_wrapper = (root.register(check_suffix), '%P')
    entry_suffix = ttk.Entry(
        root, validatecommand=check_suffix_wrapper,
        width=8, validate='key',
        justify='center', textvariable=suffix_variable
    )
    entry_suffix.grid(**kwargs)

    button_move_file = ttk.Button(
        root,
        text='Переместить'
    )
    button_move_file.grid(**kwargs, sticky='s')
    return button_move_file


def create_shortcut(
        root: tk.Frame, folders_variable: tk.StringVar,
        values: list[str], **kwargs
):
    """Комбобокс выбора папки и кнопка создания ярлыков для этой папки."""
    combobox_shortcut = ttk.Combobox(
        root,
        textvariable=folders_variable,
        state='readonly'
    )
    combobox_shortcut['values'] = values
    combobox_shortcut.grid(sticky='n', **kwargs)

    button_shortcut = ttk.Button(
        root,
        text='Создать ярлыки',
    )
    button_shortcut.grid(sticky='s', **kwargs)
    return button_shortcut
