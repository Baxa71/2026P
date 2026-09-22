class Parent:
    def __init__(self,name):
        self.name=name
    def show(self):
        print(f"Name:{self.name}")
class Child(Parent):
    pass
name=input()
obj=Child(name)
obj.show()