def sum_all_numbers(*args):
    total = sum(args)
    print(total)
def print_user_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
sum_all_numbers(1, 2, 3)
sum_all_numbers(10, 20, 30, 40, 50)

print_user_info(name="Алихан", age=19, city="Алматы")