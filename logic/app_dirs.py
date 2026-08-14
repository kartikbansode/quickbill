import os
from pathlib import Path

APP_NAME = "QuickBill"


def get_app_data_dir():
    r"""
    Returns:
    C:\Users\<User>\AppData\Local\QuickBill
    """

    base = Path(os.getenv("LOCALAPPDATA"))

    folder = base / APP_NAME

    folder.mkdir(parents=True, exist_ok=True)

    return str(folder)


def data_path(*paths):
    folder = get_app_data_dir()
    return os.path.join(folder, *paths)