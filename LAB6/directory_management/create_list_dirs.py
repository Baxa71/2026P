import os
import string
from pathlib import Path


def list_path_contents(path_str):
    path = Path(path_str)
    if not path.exists():
        print("Path does not exist.")
        return

    print("--- Directories Only ---")
    for p in path.iterdir():
        if p.is_dir():
            print(p.name)

    print("\n--- Files Only ---")
    for p in path.iterdir():
        if p.is_file():
            print(p.name)

    print("\n--- All Items (Recursive via os.walk) ---")
    for root, dirs, files in os.walk(path_str):
        print(f"Root: {root} | Dirs: {dirs} | Files: {files}")


def check_path_access(path_str):
    path = Path(path_str)
    print(f"Path: {path.absolute()}")
    print(f"Exists: {path.exists()}")
    print(f"Readable: {os.access(path, os.R_OK)}")
    print(f"Writable: {os.access(path, os.W_OK)}")
    print(f"Executable: {os.access(path, os.X_OK)}")


def test_and_split_path(path_str):
    path = Path(path_str)
    if path.exists():
        print("Path exists!")
        print(f"Parent directory: {path.parent}")
        print(f"File/folder name: {path.name}")
    else:
        print("Path does not exist.")


def generate_alphabet_files(output_dir="alphabet_files"):
    dir_path = Path(output_dir)
    dir_path.mkdir(parents=True, exist_ok=True)

    for letter in string.ascii_uppercase:
        file_path = dir_path / f"{letter}.txt"
        file_path.write_text(f"Content of file {letter}.txt\n", encoding='utf-8')
    print("Files from A.txt to Z.txt successfully created!")