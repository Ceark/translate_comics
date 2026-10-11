import tkinter as tk
from tkinter import ttk

from win32com.client import Dispatch

from custom.klass import Chapter, Comic
from custom.typing import Settings
from extract_image.functions import copy_images, unite
from extract_image.logic import orchestra


def open_main(settings: Settings):
    # Главное окно
    window = tk.Tk()
    window.title('tr_comic')
    window.geometry('300x300')
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    # Фрэйм
    mainframe = ttk.Frame(window)
    mainframe.grid(column=0, row=0, sticky='nsew')
    for i in range(2):
        mainframe.columnconfigure(i, weight=1)
    for i in range(2):
        mainframe.rowconfigure(i, weight=1)

    # Сепараторы
    sep = ttk.Separator(mainframe, orient='horizontal')
    sep.grid(column=0, row=0, columnspan=2, sticky='swe')
    sep = ttk.Separator(mainframe, orient='vertical')
    sep.grid(column=0, row=1, rowspan=1, sticky='nse')

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
        mainframe, text='Объеденить', variable=regime_var, value='union'
    )
    rad_copy.grid(column=0, row=1, sticky='nw', pady=10, padx=10)
    rad_union.grid(column=0, row=1, sticky='w', padx=10)
    func_extract = {
        'copy': copy_images,
        'union': unite
    }

    # # Кнопка экстракции
    def func_for_button_extract():
        """Функция для кнопки экстракции."""
        func = func_extract[regime_var.get()]
        comic = Comic(settings['base_dir'] / var_comics_list.get())
        orchestra(comic, func, settings['delete'], settings['original'])

    button_extract = ttk.Button(
        mainframe, command=func_for_button_extract, text='Извлечь'
    )
    button_extract.grid(column=0, row=1, padx=10, pady=10, sticky='s')

    # Добавить часть

    # Переместить изображения

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
        Функция создания ярлыка.

        - shortcut_path - адрес ярлыка;
        - target_path - файл, для которого создаётся ярлык;
        """
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target_path
        shortcut.save()

    def command_shortcut():
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
