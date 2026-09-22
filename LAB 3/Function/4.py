def filter_prime(nums):
    ans=[]
    for x in nums:
        if x<2:
            continue
        prime=True
        for i in range(2,x):
            if x%i==0:
                prime=False
                break
        if prime:
            ans.append(x)
    return ans
nums=list(map(int,input().split()))
print(filter_prime(nums))