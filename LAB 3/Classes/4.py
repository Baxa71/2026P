import math

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def show(self):
        print(self.x,self.y)
    def move(self,x,y):
        self.x=x
        self.y=y
    def dist(self,p):
        return math.sqrt((self.x-p.x)**2+(self.y-p.y)**2)
a=Point(2,3)
b=Point(5,7)
a.show()
a.move(4,6)
a.show()
print(a.dist(b))