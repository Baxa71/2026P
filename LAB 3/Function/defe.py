class Circle:
    def diameter(self, radius):
        return 3.14 * radius ** 2



r = int(input())
c1 = Circle()

print(c1.diameter(r))