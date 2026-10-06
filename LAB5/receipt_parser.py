import re
with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

items = re.findall(r"\d+\.\n([^\n]+)\n([\d\s,]+)\s*x\s*([\d\s,]+)", text)

datetime = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})", text)

payment = re.search(r"(Банковская карта|НАЛИЧНЫЕ)", text)

total = re.search(r"ИТОГО:\s*([\d\s,]+)", text)

print("Дата и время:", datetime.group(1) if datetime else "Не найдено")
print("Способ оплаты:", payment.group(1) if payment else "Не найдено")
print("Итоговая сумма:", total.group(1) if total else "Не найдено")

for item in items:
    name = item[0].strip()
    count = item[1].strip()
    price = item[2].strip()
    print(f"- {name} | {count} шт. х {price} тг")