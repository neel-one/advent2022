import sys

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]

from collections import defaultdict

dirs = set()
d = defaultdict(set)

curr = None
i = 0
while i < len(a):
    line = a[i]
    if 'cd' in line:
        c = line.split()[2]
        if c == '/':
            curr = '/'
        elif c == '..':
            curr = curr[:curr[:-1].rfind('/')+1]
        else:
            curr = curr + c + '/'
        dirs.add(curr)
        i += 1
    elif 'ls' in line:
        i += 1
        while i < len(a):
            l = a[i]
            if '$' in l:
                break
            if 'dir' in l:
                f = curr + l.split()[1] + '/'
                dirs.add(f)
                d[curr].add((f, None))
            else:
                sz, f = l.split()
                d[curr].add((f, sz))
            i += 1
dir_size = {}
ans = 0
for dr in dirs:
    total_size = 0
    s = [dr]
    while s:
        for f, sz in d[s.pop()]:
            if sz is not None:
                total_size += int(sz)
            else:
                s.append(f)
    dir_size[dr] = total_size
    if total_size <= 100000:
        ans += total_size
print(ans)

needed = 30_000_000 - (70_000_000 - dir_size['/'])
print(needed)
for k in dirs:
    if dir_size[k] < needed:
        del dir_size[k]
k = min(dir_size, key = lambda k : dir_size[k])
print(dir_size[k])
