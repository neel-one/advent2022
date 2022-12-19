import sys

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]

from collections import defaultdict
for line in a:
    d = defaultdict(int)
    t = 14
    for i in range(t):
        d[line[i]] += 1
    for i in range(t, len(line)+1):
        if len(d) == t:
            print(i)
            break
        if i == len(line):
            break
        d[line[i-t]] -= 1
        if d[line[i-t]] == 0:
            del d[line[i-t]]
        d[line[i]] += 1

