class FirstParent:
    def first(self, text1):
        print(f"First text: {text1}")
class SecondParent:
    def second(self, text2):
        print(f"Second text: {text2}")
class Child(FirstParent, SecondParent):
    pass
text1=input("first: ")
text2=input("second: ")
obj=Child()
obj.first(text1)
obj.second(text2)