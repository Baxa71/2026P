import math
def sphere_volume(r):
    return (4/3)*math.pi*r**3
r=float(input())
print(sphere_volume(r))