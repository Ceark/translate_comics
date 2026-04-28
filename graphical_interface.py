import tkinter as tk
from tkinter import filedialog

name_env = (
    'base_dir', 'original', 'editor', 'translate', 'additional_folders',
    'length_number', 'delete'
)


def create_window(column, row):
    """column - столбцы, row - строки."""
    window = tk.Tk()
    window.title('translate_comics')
    window.geometry("350x350")
    for index in range(column):  # столбцы
        window.columnconfigure(index=index, weight=1)
    for index in range(row):  # строки
        window.rowconfigure(index=index, weight=1)
    return window


window = create_window(2, 8)


# Команды для Button
def setting():
    """
    При нажатии на кнопку: собирает введённые данные и...
    1) Создает из них файл .env
    2) Возвращает данные
    """
    for string in name_env[:-1]:
        print(entries[string.upper()].get())
    print(var.get())
    # data = entries['BASE_DIR'].get()
    # test = filedialog.askdirectory()
    # print(test)
    # print(data)


# Валидация для Entry
def validate_entry(value):
    if True:
        return True
    else:
        return False


entry_validate_wrapper = (window.register(validate_entry), '%P')

# Виджеты
labels = {}
for string in name_env:
    upper = ' '.join(string.split('_')).upper()
    labels[string.upper()] = tk.Label(window, text=upper)

entries: dict = {}
for string in name_env[:-2]:
    upper = ' '.join(string.split('_')).upper()
    entries[string.upper()] = tk.Entry(window)

entries[name_env[-2].upper()] = tk.Spinbox(window, from_=1, to=5)
var = tk.BooleanVar()
entries[name_env[-1].upper()] = tk.Checkbutton(window, variable=var)

buttons = {
    'SETTING': tk.Button(window, text='Сохранить', command=setting)
}

# Засунуть в поля ввода какоенибудь значение
entries['BASE_DIR'].insert(0, 'Симферополь')

# Расположение виджетов
grid_size = window.grid_size()
for index, value in enumerate(labels):
    labels[value].grid(column=0, row=index, padx=20, sticky='w')
for index, value in enumerate(entries):
    entries[value].grid(column=1, row=index, padx=20,)
buttons['SETTING'].grid(
    column=0,
    columnspan=grid_size[0],
    row=grid_size[1] - 1
)

window.mainloop()
