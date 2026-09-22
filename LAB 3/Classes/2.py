class Shape:
    def area(self):
        print(0)
class Square(Shape):
    def __init__(self,length):
        self.length=length
    def area(self):
        print(self.length*self.length)
a=Shape()
a.area()
b=Square(5)
b.area()