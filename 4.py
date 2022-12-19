import sys

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]

def overlaps(i1, i2):
    if i1[0] <= i2[0] and i1[1] >= i2[0]:
        return True
    if i1[0] >= i2[0] and i1[1] <= i2[1]:
        return True
    if i1[0] <= i2[1] and i1[1] >= i2[1]:
        return True
    return False

total = 0
for line in a:
    i1, i2 = line.split(',')
    i1 = i1.split('-')
    i2 = i2.split('-')
    i1 = [int(v) for v in i1]
    i2 = [int(v) for v in i2]
    if overlaps(i1, i2) or overlaps(i2, i1):
        #print(i1,i2)
        total += 1
print(total)
