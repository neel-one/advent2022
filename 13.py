import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cmp_to_key

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]

@dataclass
class List:
    data: list = field(default_factory=list)

def parse(s):
    stack = []
    for i, c in enumerate(s):
        if c == '[':
            stack.append(List())
        elif c == ']':
            data = stack.pop()
            if len(stack) > 0:
                stack[-1].data.append(data)
            else:
                return data
        elif c.isdigit():
            # special case with 10 (largest number in input)
            if c == '0' and s[i-1] == '1':
                stack[-1].data[-1] = '10'
            else:
                stack[-1].data.append(c)
    return stack

def cmp_items(item1, item2):
    #print(item1,item2)
    if not isinstance(item1, List) and not isinstance(item2, List):
        a, b = int(item1), int(item2)
        if a < b:
            return 'C'
        elif a > b:
            return 'W'
        else:
            return ''
    elif isinstance(item1, List) and isinstance(item2, List):
        for i in range(max(len(item1.data), len(item2.data))):
            if i >= len(item1.data):
                return 'C'
            if i >= len(item2.data):
                return 'W'
            d = cmp_items(item1.data[i], item2.data[i])
            if d != '':
                return d
    elif not isinstance(item1, List):
        return cmp_items(List([item1]), item2)
    elif item2.isdigit():
        return cmp_items(item1, List([item2]))
    else:
        print('error')
    return ''



a = [parse(line) for line in a]
ans = 0
for i in range(0, len(a), 3):
    pair = i // 3 + 1
    result = cmp_items(a[i], a[i+1])
    #print(f'Pair {pair}: {result}')
    if result == 'C':
        ans += pair
print(ans)

def scmp(a,b):
    c = cmp_items(a,b)
    if c == 'C':
        return -1
    elif c == 'W':
        return 1
    return 0
def isdiv(p):
    return p == List([List(data=[2])]) or p == List([List(data=[6])])

a = [a[i] for i in range(len(a)) if (i+1)%3 != 0]
a.append(List([List(data=[2])]))
a.append(List([List(data=[6])]))
packets = sorted(a, key=cmp_to_key(scmp))
key = 1
for i, p in enumerate(packets):
    if isdiv(p):
        key *= (i+1)
print(key)


