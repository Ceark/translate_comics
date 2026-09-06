from pathlib import Path

from constants import path_settings
from custom_typing.custom_typing import Settings
from manage_settings.load_settings import load_settings
from window_main.window import open_main

settings: Settings = load_settings(path_settings)
Path('site_and_selectors').mkdir(exist_ok=True)

open_main(settings, path_settings)
