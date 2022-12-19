import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cmp_to_key

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
    target = 10
    size = 20
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]
    target = 2000000
    size = 4000000

@dataclass
class Interval:
    intervals: list = field(default_factory=list)
    # skip: int = None

    def merge(self):
        for i in range(len(self.intervals)-1):
            if i >= len(self.intervals)-1:
                break
            l1, r1 = self.intervals[i]
            l2, r2 = self.intervals[i+1]
            if r1 >= l2:
                self.intervals[i] = (min(l1,l2), max(r1,r2))
                self.intervals.pop(i+1)

    def update(self, x, range_):
        self._update(x, range_)
        self.merge()

    def _update(self, x, range_):
        l = x - range_
        r = x + range_
        l = max(l, 0)
        r = min(r, size)
        for i, (left, right) in enumerate(self.intervals):
            if r < left:
                self.intervals.insert(i, (l,r))
                return
            if l > right:
                continue
            if l <= right or r >= left:
                self.intervals[i] = (min(l, left), max(r,right))
                return
        self.intervals.append((l,r))


    def get_skip(self):
        l, r = self.intervals[0]
        for i, (left,right) in enumerate(self.intervals):
            if left > r+1:
                assert left-r == 2, f'{r} {left}'
                return r+1
            l = min(l,left)
            r = max(r, right)
        return None




# columns where there cannot be a beacon on row target
no_beacon = [Interval() for _ in range(size+1)]

for line in a:
    l = line.split(', ')
    l = [s.split('=') for s in l]
    sx = int(l[0][1])
    sy = int(l[1][1][:l[1][1].find(':')])
    bx = int(l[1][2])
    by = int(l[2][1])
    d = abs(sx-bx) + abs(sy-by)
    for dp in range(-d, d+1):
        i = sy + dp
        range_ = abs(d - abs(dp))
        if 0 <= i <= size:
            no_beacon[i].update(sx, range_)
            #print(no_beacon[i])
    #print('Checking next line')

#print(sorted(list(no_beacon)))
for y, ivl in enumerate(no_beacon):
    x = ivl.get_skip()
    if x is not None:
        print(x, y)
        print(4000000*x + y)
        break
