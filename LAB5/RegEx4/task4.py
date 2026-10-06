import re
p=r"[A-Z][a-z]+"
text="/Apple Banana orange Python Java"
matches = re.findall(p, text)
print("Найдены совпадения:", matches)