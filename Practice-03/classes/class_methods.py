class Account:
    def __init__(self,name,money):
        self.name=name
        self.money=money
    def deposit(self,val):
        self.money += val
        print(f"Total: {self.money}")
name =input("Name: ")
money= float(input("Money: "))
acc=Account(name, money)
val=float(input("+: "))
acc.deposit(val)