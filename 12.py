import sys
from collections import defaultdict, deque

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]


visited = set()
m, n = len(a), len(a[0])
def start_pos():
    for i in range(m):
        for j in range(n):
            if a[i][j] == 'S':
                return i, j
def get_all_start_pos():
    s = []
    for i in range(m):
        for j in range(n):
            if a[i][j] == 'a':
                s.append((i,j))
    s.append(start_pos())
    return s


def valid(v, i, j):
    if not (0 <= i < m):
        return False
    if not (0 <= j < n):
        return False
    v = a[v[0]][v[1]]
    w = a[i][j]
    if v == 'E' or w == 'S':
        return False
    if w == 'E':
        return v in ('y','z')
    if v == 'S':
        return  w in ('a','b')
    if ord(w) - ord(v) <= 1:
        #print(f'{v}->{w}')
        return True
    return False

lyr = deque(get_all_start_pos())

steps = 0
while lyr:
    nlyr = deque()
    while lyr:
        v = lyr.popleft()
        i, j = v
        if a[i][j] == 'E':
            steps -= 1
            nlyr = deque()
            break
        if v in visited:
            continue
        visited.add(v)
        i, j = v
        if valid(v, i+1,j):
            nlyr.append((i+1,j))
        if valid(v, i-1,j):
            nlyr.append((i-1,j))
        if valid(v, i,j+1):
            nlyr.append((i,j+1))
        if valid(v, i,j-1):
            nlyr.append((i,j-1))
    steps += 1
    lyr = nlyr
print(steps)




