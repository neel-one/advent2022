import sys

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]

best = []
total = 0
for c in a:
    if c == '':
        best.append(total)
        total = 0
    else:
        total += int(c)
best.append(total)
best.sort(reverse=True)
print(sum(best[:3]))
