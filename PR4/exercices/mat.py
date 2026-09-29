import math
def degree_to_radian(degree):
    return math.radians(degree)

def area_of_trapezoid(height, base1, base2):
    return 0.5 * (base1 + base2) * height

def area_of_regular_polygon(num_sides, side_length):
    return (num_sides * (side_length ** 2)) / (4 * math.tan(math.pi / num_sides))

def area_of_parallelogram(base_length, height):
    return float(base_length * height)


if __name__ == "__main__":
    degree = 15
    print(degree)
    print(f"radian: {degree_to_radian(degree):.6f}")
    print("\n")

    h, b1, b2 = 5, 5, 6
    print(f"Height:{h}")
    print(f"first:{b1}")
    print(f"second:{b2}")
    print(f"Expected:{area_of_trapezoid(h, b1, b2)}")
    print("\n")

    num_sides = 4
    side_len = 25
    print(f"Input number of sides: {num_sides}")
    print(f"Input the length of a side: {side_len}")
    print(f"The area of the polygon is: {area_of_regular_polygon(num_sides, side_len):.0f}")
    print("\n")

    base = 5
    height = 6
    print(f"Length:{base}")
    print(f"Height of parallelogram: {height}")
    print(f"Expected: {area_of_parallelogram(base, height)}")