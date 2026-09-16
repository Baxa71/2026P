import random
secret=random.randint(1,10)
num=0
while(num!=secret):
    num=int(input())
    if(num>secret):
        print(">")
    elif(num<secret):
        print("<")
print(f"Yes {secret}")