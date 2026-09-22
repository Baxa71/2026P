num=input()
numbers=[int(x) for x in num.split()]
even=list(filter(lambda num: num%2==0, numbers))
print(even)