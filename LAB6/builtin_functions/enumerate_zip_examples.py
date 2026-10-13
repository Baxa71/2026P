names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

print("--- enumerate() example ---")
for index, name in enumerate(names, start=1):
    print(f"{index}. {name}")

print("\n--- zip() example ---")
for name, score in zip(names, scores):
    print(f"{name} scored {score} points")

print("\n--- sorted() and type conversion ---")
mixed_nums = [5, 2, 9, 1, 5, 6]
print("Sorted (descending):", sorted(mixed_nums, reverse=True))
print("Type conversion (float to int):", int(9.87))
print("Type check:", type(mixed_nums) is list)