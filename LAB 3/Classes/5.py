class Account:
    def __init__(self,owner,balance=0):
        self.owner=owner
        self.balance=balance
    def deposit(self,money):
        self.balance+=money
        print("Balance:",self.balance)
    def withdraw(self,money):
        if money<=self.balance:
            self.balance-=money
            print("Balance:",self.balance)
        else:
            print("Not enough money")
a=Account("KBTU",1000)
a.deposit(500)
a.deposit(300)
a.withdraw(400)
a.withdraw(2000)