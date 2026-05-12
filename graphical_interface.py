import tkinter as tk
from tkinter import filedialog

name_env = (
    'BASE_DIR', 'ORIGINAL', 'EDITOR', 'TRANSLATE', 'ADDITIONAL_FOLDERS',
    'LENGTH_NUMBER', 'DELETE'
)


def create_window(column, row):
    window = tk.Tk()
    window.title('translate_comics')
    window.geometry("350x350")
    for index in range(column):  # столбцы
        window.columnconfigure(index=index, weight=1)
    for index in range(row):  # строки
        window.rowconfigure(index=index, weight=1)
    return window


def create_labels(window, strings):
    labels = {
        value: tk.Label(window, text=value)
        for value
        in strings
    }
    for index, key in enumerate(labels):
        labels[key].grid(column=0, row=index, padx=20, sticky='w')
    return labels


def create_entries(window, strings):
    # Засунуть в поля ввода какое-нибудь значение
    # entries['BASE_DIR'].insert(0, 'Симферополь')
    entries = {
        value: tk.Entry(window)
        for value
        in strings
    }
    for index, key in enumerate(entries):
        entries[key].grid(column=1, row=index, padx=20)
    return entries


def setting(strings=name_env):
    """
    При нажатии на кнопку: собирает введённые данные и...
    1) Создает из них файл .env
    2) Возвращает данные
    """
    dictionary = {
        string: entries[string].get()
        for string
        in strings
    }
    global sirop
    sirop = dictionary
    window.destroy()


def create_buttons(window, grid_size=(2, 8)):
    button = tk.Button(window, text='Сохранить', command=setting)
    button.grid(
        column=0,
        columnspan=grid_size[0],
        row=grid_size[1] - 1
    )
    return button


sirop = ''
window = create_window(2, 8)
labels = create_labels(window, name_env)
entries = create_entries(window, name_env)
button = create_buttons(window, window.grid_size())
window.mainloop()
print(sirop)
