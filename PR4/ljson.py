import json

json_data = '{"name": "Ali", "age": 20}'
data = json.loads(json_data)
print("Name:", data["name"])
print("Age:", data["age"])
new_json = json.dumps(data)
print("JSON string:", new_json)