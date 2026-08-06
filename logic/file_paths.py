import os
import sys


def app_path(*paths):
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(sys.argv[0]))

    return os.path.join(base, *paths)