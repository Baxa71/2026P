with open("sample.txt", "w", encoding="utf-8") as f:
    f.write("Line 1: Hello, Python!\n")
    f.write("Line 2: File handling is easy.\n")

with open("sample.txt", "a", encoding="utf-8") as f:
    f.write("Line 3: Appended new content.\n")

print("File written and appended successfully.")