import re
def camee(camel):
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', camel)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
text = "camelCaseToSnakeCase"
print(camee(text))