import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cmp_to_key

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]


grid = [['.' for _ in range(1000)] for _ in range(160)]
m = 0
for i, line in enumerate(a):
    pairs = line.split(' -> ')
    for i, pair in enumerate(pairs):
        if i == 0:
            continue
        x, y = pair.split(',')
        x0, y0 = pairs[i-1].split(',')
        x, y, x0, y0 = int(x), int(y), int(x0), int(y0)
        m = max(m, max(y,y0))
        if x == x0:
            s, e = min(y,y0), max(y,y0)+1
            for i in range(s, e):
                grid[i][x] = '#'
        elif y == y0:
            s, e = min(x,x0), max(x,x0)+1
            for j in range(s, e):
                grid[y][j] = '#'

for j in range(len(grid[-1])):
    grid[m+2][j] = '#'

def p():
    for i, row in enumerate(grid):
        if i >= 13:
            continue
        r = ''.join(row[494:504])
        print(f'{i} {r}')

def solve(grid):
    sand = 0
    while True:
        y, x = 0, 500
        if grid[y][x] == 'o':
            return sand
        while True:
            if grid[y][x] == '.':
                #print(y+1, x+1)
                if grid[y+1][x] == '.':
                    y = y+1
                elif grid[y+1][x-1] == '.':
                    y = y+1
                    x = x-1
                elif grid[y+1][x+1] == '.':
                    y = y+1
                    x = x+1
                else:
                    grid[y][x] = 'o'
                    break
            else:
                break
        sand += 1

s = solve(grid)
#p()
print(s)
