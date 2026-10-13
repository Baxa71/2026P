from pathlib import Path

def count_file_lines(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f)
        print(f"Line count in {filepath}: {line_count}")
        return line_count
    except FileNotFoundError:
        print(f"File not found: {filepath}")

def write_list_to_file(filepath, data_list):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines([f"{item}\n" for item in data_list])
    print(f"Successfully wrote {len(data_list)} items to {filepath}")