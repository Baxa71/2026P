import re
p=r"^a.*b$"
tes=["acb","a123b","a_b","ax"]
for s in tes:
    print(f"'{s}': {bool(re.fullmatch(p, s))}")