import sys

if len(sys.argv) == 1:
    a = [line for line in open('in').readlines()]
else:
    a = [line for line in open(__file__.rstrip('.py')).readlines()]

from collections import defaultdict, deque

d = defaultdict(deque)
for line in a:
    if '[' not in line:
        break
    for i in range(1, len(line), 4):
        if line[i] != ' ':
            stack = (i-1)//4+1
            d[stack].appendleft(line[i])
for k in d:
    d[k] = list(d[k])

for line in a:
    if 'move' in line:
        line = line.split()
        quantity = int(line[1])
        src = int(line[3])
        dst = int(line[5])
        d[dst].extend(d[src][-quantity:])
        d[src] = d[src][:-quantity]

for key in sorted(d.keys()):
    print(d[key][-1], end='')
print()
