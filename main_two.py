import json
import tkinter as tk
from functools import partial
from pathlib import Path

from custom_typing import PythonTwoSettings
from load_settings import load_settings
from window_main.window import open_main

path_settings = Path('settings.json')
settings: PythonTwoSettings = load_settings(path_settings)

open_main(settings, path_settings)
