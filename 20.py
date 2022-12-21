import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cmp_to_key
from copy import deepcopy

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]

def parse():
    nums = []
    for line in a:
        nums.append(Num(int(line), len(nums)))
    return nums

@dataclass
class Num:
    value: int
    id: int

def solve(nums):
    for moved in range(len(nums)):
        i = None
        for j, n in enumerate(nums):
            if n.id == moved:
                i = j
                break
        assert i is not None
        num = nums[i]
        nums.pop(i)
        j = (i + num.value) % len(nums)
        if j == 0:
            j += len(nums)
        nums.insert(j, num)
        #print([n.value for n in nums])
    i = None
    for j, num in enumerate(nums):
        if num.value == 0:
            i = j
            break
    return nums[(i+1000)%len(nums)].value + nums[(i+2000)%len(nums)].value + nums[(i+3000)%len(nums)].value

def part1():
    nums = parse()
    return solve(nums)

def part2():
    nums = parse()
    key = 811589153
    for i in range(len(nums)):
        nums[i].value *= key
    for _ in range(10):
        a = solve(nums)
    return a



#print(f'Part 1: {part1()}')
print(f'Part 2: {part2()}')