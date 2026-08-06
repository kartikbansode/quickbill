import os
import sys


APP_NAME = "QuickBill"


def resource_path(*paths):
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        base = os.path.abspath(".")

    return os.path.join(base, *paths)


def data_path(*paths):
    if os.name == "nt":
        base = os.path.join(
            os.environ["LOCALAPPDATA"],
            APP_NAME,
        )
    else:
        base = os.path.join(
            os.path.expanduser("~"),
            f".{APP_NAME.lower()}",
        )

    os.makedirs(base, exist_ok=True)

    return os.path.join(base, *paths)