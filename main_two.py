from constants import path_settings
from custom_typing_.custom_typing import Settings
from manage_settings.load_settings import load_settings
from window_main_.window import open_main

settings: Settings = load_settings(path_settings)

open_main(settings, path_settings)
