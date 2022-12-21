import math

def getNextNumber(N):
    nums = [int(i) for i in str(N)]
    for i in range(len(nums) - 1, -1, -1):
        if nums[i] != 9:
            nums[i] += 1
            res = 0
            # print(nums[i])
            for j in range(len(nums)):
                res = (res * 10) + nums[j]
                # print(res)
            return res

    return N + int(math.pow(10, len(nums)))

def getSum(N):
    return sum([int(i) for i in str(N)])

def solution(N):
    original_sum = getSum(N)
    while(getSum(N) != 2*original_sum):
        N = getNextNumber(N)
    return N

print(solution(499))
