def square_generator(n):
    for i in range(1, n + 1):
        yield i ** 2


def even_generator(n):
    for i in range(0, n + 1, 2):
        yield i


def divisible_by_3_and_4(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2


def countdown(n):
    while n >= 0:
        yield n
        n -= 1


if __name__ == "__main__":
    for val in square_generator(5):
        print(val, end=" ")
    print("\n")

    try:
        user_input = int(input("Enter "))
        print(",".join(str(num) for num in even_generator(user_input)))
    except ValueError:
        print("Invalid input! Skipping interactive input...")
    print("\n")

    for num in divisible_by_3_and_4(50):
        print(num, end=" ")
    print("\n")

    for sq in squares(3, 7):
        print(sq, end=" ")
    print("\n")

    for count in countdown(5):
        print(count, end=" ")
    print("\n")