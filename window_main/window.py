import re
import tkinter as tk
from shutil import move
from tkinter import ttk

from win32com.client import Dispatch

from custom.klass import Comic
from custom.typing import Settings
from extract_image.functions import copy_images, unite
from extract_image.logic import orchestra


def open_main(settings: Settings):
    # Главное окно
    window = tk.Tk()
    window.title('tr_comic')
    window.geometry('355x300')
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    # Фрэйм
    mainframe = ttk.Frame(window)
    mainframe.grid(column=0, row=0, sticky='nsew')
    for i in range(2):
        mainframe.columnconfigure(i, weight=1)
    for i in range(3):
        mainframe.rowconfigure(i, weight=1)

    # Сепараторы
    # Горизонтальный
    for i in range(2):
        sep = ttk.Separator(mainframe, orient='horizontal')
        sep.grid(column=0, row=i, columnspan=2, sticky='swe')
    # Вертикальный
    for i in range(1):
        sep = ttk.Separator(mainframe, orient='vertical')
        sep.grid(column=i, row=1, rowspan=2, sticky='nse')

    # Выпадающий список комиксов
    var_comics_list = tk.StringVar()
    list_comics = [
        value.name
        for value
        in settings['base_dir'].iterdir()
        if Comic(value).is_comic()
    ]
    if len(list_comics):
        var_comics_list.set(list_comics[0])
    combobox_list_comics = ttk.Combobox(
        mainframe,
        textvariable=var_comics_list,
        state='readonly'
    )
    combobox_list_comics['values'] = list_comics
    combobox_list_comics.grid(column=0, row=0, columnspan=2)

    # Экстракция
    # # Выбор режима экстракции
    regime_var = tk.StringVar(value='copy')
    rad_copy = ttk.Radiobutton(
        mainframe, text='Копировать', variable=regime_var, value='copy'
    )
    rad_union = ttk.Radiobutton(
        mainframe, text='Объединить', variable=regime_var, value='union'
    )
    rad_copy.grid(column=0, row=1, sticky='nw', pady=10, padx=10)
    rad_union.grid(column=0, row=1, sticky='w', padx=10)
    func_extract = {
        'copy': copy_images,
        'union': unite
    }

    # # Кнопка экстракции
    def command_extract():
        """Функция для кнопки экстракции."""
        func = func_extract[regime_var.get()]
        comic = Comic(settings['base_dir'] / var_comics_list.get())
        orchestra(comic, func, settings['delete'], settings['original'])

    button_extract = ttk.Button(
        mainframe, command=command_extract, text='Извлечь'
    )
    button_extract.grid(column=0, row=1, padx=10, pady=10, sticky='s')

    # Добавить часть
    # # Сколько частей добавлять
    def check_num(newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval) <= 5
    check_num_wrapper = (mainframe.register(check_num), '%P')

    var_add_chapter = tk.IntVar(value=1)
    entry_add_chapter = tk.Entry(
        mainframe, textvariable=var_add_chapter,
        validate='key', validatecommand=check_num_wrapper,
        width=10, justify='center'
    )
    entry_add_chapter.grid(column=0, row=2, sticky='n', padx=5, pady=5)

    def command_add_chapter():
        """Функция для кнопки добавления части."""
        comic = Comic(settings['base_dir'] / var_comics_list.get())
        quantity = var_add_chapter.get()
        comic.create_chapters(quantity)

    button_add_chapter = ttk.Button(
        mainframe,
        command=command_add_chapter,
        text='Добавить часть'
    )
    button_add_chapter.grid(column=0, row=2, sticky='s', padx=5, pady=5)

    # Переместить изображения
    var_where_from = tk.StringVar(value=settings['editor'])
    var_where_to = tk.StringVar(value=settings['translate'])
    var_suffix = tk.StringVar(value='*.png')

    values = [
        settings['original'],
        settings['editor'],
        settings['translate']
    ] + settings['other_folder']
    combobox_where_from = ttk.Combobox(
        mainframe,
        textvariable=var_where_from,
        state='readonly',
        width=10,
        values=values
    )
    combobox_where_from.grid(column=1, row=2, padx=5, pady=5, sticky='nw')
    combobox_where_to = ttk.Combobox(
        mainframe,
        textvariable=var_where_to,
        state='readonly',
        width=10,
        values=values
    )
    combobox_where_to.grid(column=1, row=2, padx=5, pady=5, sticky='ne')

    symbol_arrow = tk.Label(mainframe, text='\u279d')
    symbol_arrow.grid(column=1, row=2, padx=5, pady=5, sticky='n')

    def check_suffix(newval):
        return re.match(r'^\*\..*$', newval) is not None
    check_suffix_wrapper = (mainframe.register(check_suffix), '%P')

    entry_suffix = ttk.Entry(
        mainframe, validatecommand=check_suffix_wrapper,
        width=8, validate='key',
        justify='center', textvariable=var_suffix
    )
    entry_suffix.grid(column=1, row=2)

    def command_move_files():
        comic = Comic(settings['base_dir'] / var_comics_list.get())
        folder_from = var_where_from.get()
        folder_to = var_where_to.get()
        suffix = var_suffix.get()
        for chapter in comic.list_chapters():
            for fl in (comic / chapter / folder_from).glob(suffix):
                move(
                    fl,
                    comic / chapter / folder_to
                )

    button_move_file = ttk.Button(
        mainframe,
        command=command_move_files,
        text='Переместить'
    )
    button_move_file.grid(column=1, row=2, sticky='s', pady=5)

    # Создать ярлыки
    # # Выпадающий список с техническими папками
    var_tech_folders_shortcut = tk.StringVar()
    combobox_shortcut = ttk.Combobox(
        mainframe,
        textvariable=var_tech_folders_shortcut,
        state='readonly'
    )
    combobox_shortcut['values'] = Comic.technical_folders
    if len(combobox_shortcut['values']):
        var_tech_folders_shortcut.set(combobox_shortcut['values'][0])
    combobox_shortcut.grid(column=1, row=1, pady=5, sticky='n')

    # # Кнопка создания ярлыков
    def shortcut(shortcut_path: str, target_path: str):
        """
        Функция создания ярлыка, Windows.

        - shortcut_path - адрес ярлыка;
        - target_path - файл, для которого создаётся ярлык;
        """
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target_path
        shortcut.save()

    def command_shortcut():
        """Команда для кнопки создания ярлыков, только для Windows."""
        comic = Comic(settings['base_dir'] / var_comics_list.get())
        shortcut_folder = comic / var_tech_folders_shortcut.get()
        shortcut_folder.mkdir(exist_ok=True)
        for chapter in comic.list_chapters():
            chapter_folder = chapter / combobox_shortcut.get()
            chapter_folder.mkdir(exist_ok=True)
            for obj in chapter_folder.iterdir():
                shortcut_name = str(chapter.number) + '_' + obj.stem + '.lnk'
                shortcut_path = shortcut_folder / shortcut_name
                shortcut(
                    shortcut_path=str(shortcut_path),
                    target_path=str(obj)
                )

    button_shortcut = ttk.Button(
        mainframe, text='Создать ярлыки', command=command_shortcut
    )
    button_shortcut.grid(column=1, row=1, pady=5, sticky='s')

    # Запуск окна
    window.mainloop()
