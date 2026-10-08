import tkinter as tk
from tkinter import ttk

from custom.klass import Comic
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
    rad_copy.grid(column=0, row=1, sticky='nw', pady=5, padx=5)
    rad_union.grid(column=0, row=1, sticky='ne', pady=5, padx=5)
    func_extract = {
        'copy': copy_images,
        'union': unite
    }

    # # Кнопка экстракции
    def func_for_button_extract():
        func = func_extract[regime_var.get()]
        comic = Comic(settings['base_dir'] / var_comics_list.get())
        orchestra(comic, func, settings['delete'], settings['original'])

    button_extract = ttk.Button(
        mainframe, command=func_for_button_extract, text='Извлечь'
    )
    button_extract.grid(column=0, row=1, padx=5, pady=10)

    window.mainloop()
