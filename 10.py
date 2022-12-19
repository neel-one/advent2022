import sys

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]
from collections import defaultdict
X = 1
d = defaultdict(list)
signal = 0
cycle = 1
def check_cycle():
    global signal, cycle, X
    if (cycle-20)%40 == 0:
        signal += X * cycle
def inc():
    global cycle
    drawing = (cycle) % 40
    if drawing-1 <= X <= drawing+1:
        print('#',end='')
    else:
        print('.',end='')
    cycle += 1
    if (cycle)%40 == 0:
        print()

print('#',end='')
for line in a:
    check_cycle()
    if 'addx' in line:
        _, v = line.split()
        inc()
        check_cycle()
        X += int(v)
    inc()
while cycle < 241:
    check_cycle()
    inc()
print()
print(signal)
