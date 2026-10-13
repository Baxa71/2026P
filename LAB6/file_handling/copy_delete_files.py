import os
import shutil
from pathlib import Path


def copy_file(src, dst):
    try:
        shutil.copy(src, dst)
        print(f"File copied from {src} to {dst}")
    except Exception as e:
        print(f"Error copying file: {e}")


def safe_delete(filepath):
    path = Path(filepath)
    if not path.exists():
        print(f"Deletion cancelled: path {filepath} does not exist.")
        return
    if not os.access(path, os.W_OK):
        print("Deletion cancelled: write/delete permissions missing.")
        return

    path.unlink()
    print(f"File {filepath} successfully deleted.")