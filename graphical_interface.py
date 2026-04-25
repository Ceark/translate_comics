import tkinter as tk
from tkinter import filedialog

# Окно
window = tk.Tk()
window.title('translate_comics')
window.geometry("350x350")  # Ширина - высота

# Столбцы и строки
quantity_column = 2
quantity_row = 8
for index in range(quantity_column):
    window.columnconfigure(index=index, weight=1)
for index in range(quantity_row):
    window.rowconfigure(index=index, weight=1)


# Команды для Button
def setting():
    """
    При нажатии на кнопку: собирает введённые данные и...
    1) Создает из них файл .env
    2) Возвращает данные
    """
    data = entries['BASE_DIR'].get()
    test = filedialog.askdirectory()
    print(test)
    print(data)


# Валидация для Entry
def validate_entry(value):
    if True:
        return True
    else:
        return False


entry_validate_wrapper = (window.register(validate_entry), '%P')

# Виджеты
labels = {}
name_env = (
    'base_dir', 'original', 'editor', 'translate', 'additional_folders',
    'length_number', 'delete'
)
for string in name_env:
    upper = ' '.join(string.split('_')).upper()
    labels[string.upper()] = tk.Label(window, text=upper)

entries: dict = {}
for string in name_env[:-2]:
    upper = ' '.join(string.split('_')).upper()
    entries[string.upper()] = tk.Entry(window)

entries['length_number'] = tk.Spinbox(window, from_=1, to=5)
var = tk.BooleanVar()
entries['delete'] = tk.Checkbutton(window, variable=var)

buttons = {
    'SETTING': tk.Button(window, text='Сохранить', command=setting)
}

# Засунуть в поля ввода какоенибудь значение
entries['BASE_DIR'].insert(0, 'Симферополь')

# Расположение виджетов
for index, value in enumerate(labels):
    labels[value].grid(column=0, row=index, padx=20, sticky='w')
for index, value in enumerate(entries):
    entries[value].grid(column=1, row=index, padx=20,)
buttons['SETTING'].grid(
    column=0,
    columnspan=quantity_column,
    row=(quantity_row-1)
)

window.mainloop()
