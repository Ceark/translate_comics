import tkinter as tk

# Окно
window = tk.Tk()
window.title('translate_comics')
window.geometry("300x200")

# Столбцы и строки
window.columnconfigure(index=0, weight=1)
window.columnconfigure(index=1, weight=1)
window.rowconfigure(index=0, weight=1)
window.rowconfigure(index=1, weight=1)


# Команды для Button
def setting():
    """
    При нажатии на кнопку: собирает введённые данные и...
    1) Создает из них файл .env
    2) Возвращает данные
    """
    data = entries['BASE_DIR'].get()
    print(data)


# Валидация для Entry
def validate_entry(value):
    if True:
        return True
    else:
        return False


entry_validate_wrapper = (window.register(validate_entry), '%P')

# Виджеты
labels = {
    'BASE_DIR': tk.Label(window, text='BASE DIR')
}
entries = {
    'BASE_DIR': tk.Entry(
        window,
        validate='key',
        validatecommand=entry_validate_wrapper
    ),
    'ORIGINAL': tk.Entry(
        window
    )
}
buttons = {
    'SETTING': tk.Button(window, text='Сохранить', command=setting)
}

# Засунуть в поля ввода какоенибудь значение
entries['BASE_DIR'].insert(0, 'Симферополь')

# Расположение виджетов
labels['BASE_DIR'].grid(column=0, row=0)
entries['BASE_DIR'].grid(column=1, row=0)
buttons['SETTING'].grid(column=0, columnspan=2, row=1)

window.mainloop()
