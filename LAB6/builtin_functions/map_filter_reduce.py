from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

squared = list(map(lambda x: x ** 2, numbers))
print("Squared:", squared)

evens_list = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", evens_list)

total_sum = reduce(lambda x, y: x + y, numbers)
print("Sum via reduce:", total_sum)