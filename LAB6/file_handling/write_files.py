from pathlib import Path

file_path = Path("sample.txt")

if file_path.exists():
    with open(file_path, "r", encoding="utf-8") as f:
        print(f.read())

    with open(file_path, "r", encoding="utf-8") as f:
        print(f.readline(), end="")
        print(f.readline(), end="")

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        print(f"Total lines: {len(lines)}")
        print("Lines list:", lines)