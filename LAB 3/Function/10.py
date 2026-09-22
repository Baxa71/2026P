def unique(nums):
    ans=[]
    for x in nums:
        if x not in ans:
            ans.append(x)
    return ans
nums=list(map(int,input().split()))
print(unique(nums))