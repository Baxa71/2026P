class Parent:
    def __init__(self,name):
        self.name=name
class Child(Parent):
    def __init__(self,name,age):
        super().__init__(name)
        self.age=age
    def show(self):
        print(f"Name:{self.name},Age:{self.age}")
name=input("name:")
age=input("age:")
obj=Child(name, age)
obj.show()