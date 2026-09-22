class Car:
    def __init__(self,brand,year):
        self.brand=brand
        self.year=year
car_brand = input()
car_year = int(input())
c = Car(car_brand, car_year)
print(c.brand,c.year)