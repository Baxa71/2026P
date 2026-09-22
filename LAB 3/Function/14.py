def grams_to_ounces(grams):
    return 28.3495231*grams
def sphere_volume(r):
    import math
    return (4/3)*math.pi*r**3
def has_33(nums):
    for i in range(len(nums)-1):
        if nums[i]==3 and nums[i+1]==3:
            return True
    return False