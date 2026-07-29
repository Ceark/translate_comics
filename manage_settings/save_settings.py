import json
from pathlib import Path

from custom_typing.custom_typing import Settings, SettingsVar


def default_for_path(obj):
    """
    Обработка объектов Path для json.
    """
    if isinstance(obj, Path):
        return f"{obj._raw_path}"
    raise TypeError(f'Cannot serialize object of {type(obj)}')


def save_dict_settings(path: Path, settings: Settings, widgets: SettingsVar):
    """
    Сохранить словарь настроек как json-файл.
    """
    update_settings = Settings(
        base_dir=Path(widgets['base_dir'].get()),
        original=widgets['original'].get(),
        editor=widgets['editor'].get(),
        translate=widgets['translate'].get(),
        other_folder=widgets['other_folder'].get().split(', '),
        delete=widgets['delete'].get(),
        length_number=widgets['length_number'].get()
    )
    # Альтернативный вариант, но на него ругается MyPy
    """
    update_settings = {
        key: widgets[key].get()
        for key
        in (Settings.__required_keys__)
    }
    update_settings['base_dir'] = Path(widgets['base_dir'].get())
    update_settings['other_folder'] = widgets['other_folder'].get().split(', ')
    """
    settings.update(update_settings)
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(
            update_settings, file, indent=4, ensure_ascii=False,
            default=default_for_path
        )
