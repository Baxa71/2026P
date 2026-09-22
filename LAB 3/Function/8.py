def spy_game(nums):
    x=0
    for n in nums:
        if x==0 and n==0:
            x=1
        elif x==1 and n==0:
            x=2
        elif x==2 and n==7:
            return True
    return False
print(spy_game([1,2,4,0,0,7,5]))
print(spy_game([1,0,2,4,0,5,7]))
print(spy_game([1,7,2,0,4,5,0]))