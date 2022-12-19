import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cmp_to_key

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]


@dataclass
class Grid:
    grid = [[[None for _ in range(22)] for _ in range(22)] for _ in range(22)]

    def valid(self, i, j, k):
        return 0 <= i < 22 and 0 <= j < 22 and 0 <= k < 22 

    def set(self, v, i, j, k):
        if self.valid(i, j, k):
            self.grid[i][j][k] = v
    
    def get(self, i, j, k):
        if self.valid(i, j, k):
            return self.grid[i][j][k]
        return None

def build_grid(grid=None):
    grid = grid or Grid()
    for line in a:
        x,y,z = (int(v) for v in line.split(','))
        grid.set('N', x, y, z)
    return grid

def part1():
    grid = build_grid()
    total = 0
    for i in range(22):
        for j in range(22):
            for k in range(22):
                if not grid.get(i,j,k):
                    continue
                sa = 6
                for offset in (-1,1):
                    if grid.get(i+offset, j, k):
                        sa -= 1
                    if grid.get(i, j+offset, k):
                        sa -= 1
                    if grid.get(i, j, k+offset):
                        sa -= 1
                #print(sa)
                total += sa
    return total

def build_full_grid():
    grid = Grid()
    for i in range(22):
        for j in range(22):
            for k in range(22):
                grid.set('n',i,j,k)
    return build_grid(grid)

def part2():
    grid = build_full_grid()
    debug = 0
    s = [(i,0,0) for i in range(22)] + [(0,j,0) for j in range(22)] + [(0,0,k) for k in range(22)]
    while s:
        top = s.pop()
        i, j, k = top
        v = grid.get(*top)
        if v in ('n', 'N'):
            if v == 'n':
                grid.set('v', *top)
                for offset in (-1,1):
                    s.append((i+offset, j, k))
                    s.append((i,j+offset,k))
                    s.append((i,j,k+offset))
            else:
                grid.set('V', *top)
    total = 0
    for i in range(22):
        for j in range(22):
            for k in range(22):
                if grid.get(i,j,k)  != 'V':
                    continue
                debug += 1
                sa = 0
                for offset in (-1,1):
                    if grid.get(i+offset, j, k) in ('v',None):
                        sa += 1
                    if grid.get(i, j+offset, k) in ('v',None):
                        sa += 1
                    if grid.get(i, j, k+offset) in ('v',None):
                        sa += 1
                #print(sa)
                total += sa
    print(debug)
    return total
    


print(f'Part 1: {part1()}')
print(f'Part 2: {part2()}')