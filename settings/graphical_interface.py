import tkinter as tk
from tkinter import ttk
from pathlib import Path


def parameters_env_new():
    padx = 10
    pady = 5
    return_data: dict = {}

    window = tk.Tk()
    window.title('Настройки')
    window.geometry('250x500')

    for index in range(2):
        window.columnconfigure(index=index, weight=1)
    for index in range(8):
        window.rowconfigure(index=index, weight=1)
    # column_label = 1
    # column_input = 2
    # weight = 1
    # for index in range(2):
    #     window.columnconfigure(1, 1)
    # for index in range(8):
    #     window.rowconfigure(1, 1)

    # named_dirs = (
    #     'ORIGINAL',
    #     'EDITOR',
    #     'TRANSLATE'
    # )
    # for index, name in enumerate(named_dirs, start=2):
    #     return_data[name] = tk.Label(window, text=name)
    #     return_data[name].grid(row=index, column=column_label)

    # for c in range(3):
    #     window.columnconfigure(index=c, weight=1)
    # for r in range(3):
    #     window.rowconfigure(index=r, weight=1)

    for r in range(8-1):
        for c in range(2):
            label = tk.Label(text=f"({r},{c})")
            # btn = ttk.Button(text=f"({r},{c})")
            label.grid(row=r, column=c)

    # Button
    def button_save():
        pass

    button = tk.Button(window, text='Сохранить', command=button_save)
    button.grid(row=8-1, column=0, columnspan=2)
    window.mainloop()


def parameters_env():
    return_data = []

    padx = 10
    pady = 5

    window = tk.Tk()
    window.title('Настройки')
    window.geometry('250x500')

    # BASE DIR
    label_base_dir = tk.Label(window, text='BASE DIR')
    label_base_dir.pack(padx=padx, pady=pady, anchor='w')

    entry_base_dir = tk.Entry(window)
    entry_base_dir.pack(padx=padx, anchor='w')

    # ORIGINAL
    label_original = tk.Label(window, text='ORIGINAL')
    label_original.pack(padx=padx, pady=pady, anchor='w')

    entry_original = tk.Entry(window)
    entry_original.pack(padx=padx, anchor='w')

    # EDITOR
    label_editor = tk.Label(window, text='EDITOR')
    label_editor.pack(padx=padx, pady=pady, anchor='w')

    entry_editor = tk.Entry(window)
    entry_editor.pack(padx=padx, anchor='w')

    # TRANSLATE
    label_translate = tk.Label(window, text='TRANSLATE')
    label_translate.pack(padx=padx, pady=pady, anchor='w')

    entry_translate = tk.Entry(window)
    entry_translate.pack(padx=padx, anchor='w')

    # ADDITIONAL_FOLDERS
    label_additional_folders = tk.Label(window, text='ADDITIONAL_FOLDERS')
    label_additional_folders.pack(padx=padx, pady=pady, anchor='w')

    entry_additional_folders = tk.Entry(window)
    entry_additional_folders.pack(padx=padx, anchor='w')

    # LENGTH NUMBER
    label_length_number = tk.Label(window, text='LENGTH NUMBER')
    label_length_number.pack(padx=padx, pady=pady, anchor='w')

    length_number_spinbox = tk.Spinbox(window, from_=1, to=5)
    length_number_spinbox.pack(padx=padx, pady=pady, anchor='w')

    # DELETE
    label_delete = tk.Label(window, text='DELETE')
    label_delete.pack(padx=padx, pady=pady, anchor='w')

    var = tk.BooleanVar()
    delete_checkbutton = tk.Checkbutton(
        window,
        text='Удалять файлы после обработки',
        variable=var
    )
    delete_checkbutton.pack(padx=padx, pady=pady, anchor='w')

    # Button
    def button_save():
        nonlocal return_data
        return_data = {
            'BASE_DIR': entry_base_dir.get(),
            'ORIGINAL': entry_original.get(),
            'EDITOR': entry_editor.get(),
            'TRANSLATE': entry_translate.get(),
            'ADDITIONAL_FOLDERS': entry_additional_folders.get(),
            'LENGTH_NUMBER': length_number_spinbox.get(),
            'DELETE': var.get(),
        }
        window.destroy()

    button = tk.Button(window, text='Сохранить', command=button_save)
    button.pack(padx=padx, pady=pady, anchor='se')

    window.mainloop()
    return return_data


print(parameters_env_new())
