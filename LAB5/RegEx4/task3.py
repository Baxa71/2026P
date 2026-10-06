import re
p = r"[a-z]+_[a-z]+"
text = "hello_world, Python_code, test_case_example"
matches = re.findall(p, text)
print("Найдены совпадения:", matches)