temps=input()
celsius_temps = [float(x) for x in temps.split()]
f_temps = list(map(lambda c: (c * 9/5) + 32, celsius_temps))
print(f_temps)