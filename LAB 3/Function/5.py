def permutations(s):
    if len(s)==1:
        return [s]
    ans=[]
    for i in range(len(s)):
        x=s[i]
        rest=s[:i]+s[i+1:]
        for p in permutations(rest):
            ans.append(x+p)
    return ans

s=input()
for x in permutations(s):
    print(x)