import sys

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]

#print(a)
total = 0
for i in range(0, len(a), 3):
    first = a[i]
    for c in first:
        if c in a[i+1] and c in a[i+2]:
            order = ord(c) - ord('a')
            if 0 <= order < 26:
                total += order + 1
            else:
                total += ord(c)-ord('A') + 27
            break
print(total)
