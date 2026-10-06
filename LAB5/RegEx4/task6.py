import re
text="Python, Reg. P Tasf 6"
result=re.sub(r"[\s,\.]", ":", text)
print(result)