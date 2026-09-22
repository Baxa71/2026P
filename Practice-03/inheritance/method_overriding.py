class Parent:
    def action(self):
        print("")
class Child(Parent):
    def __init__(self, name):
        self.name = name
    def action(self):
        print(self.name)
name=input("name: ")
obj= Child(name)
obj.action()