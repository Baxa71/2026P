import re
text="SplitStringAtUppercaseLetters"
parts=re.findall(r'[A-Z][^A-Z]*', text)
print(parts)