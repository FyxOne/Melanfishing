import sys, os

def resource_path(relative_path):
    """Возвращает абсолютный путь к ресурсу (работает и для .exe, и для исходников)."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
