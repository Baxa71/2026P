import re
p = r"^ab{2,3}$"
tes = ["ab", "abb", "abbb", "abbbb"]
for s in tes:
    print(f"'{s}': {bool(re.fullmatch(p, s))}")