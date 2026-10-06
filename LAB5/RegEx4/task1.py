import re
p=r"^ab*$"
tes=["a","ab","abbb","b","abc"]
for s in tes:
    print(f"'{s}': {bool(re.fullmatch(p   , s))}")