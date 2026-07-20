from typing import TypedDict
from pathlib import Path


class PythonSettings(TypedDict):
    base_dir: str
    original: str
    editor: str
    translate: str
    other_folder: str
    delete: bool
    length_number: int


class PythonTwoSettings(TypedDict):
    base_dir: Path
    original: str
    editor: str
    translate: str
    other_folder: list[str]
    delete: bool
    length_number: int
