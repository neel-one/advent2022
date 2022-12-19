import sys

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]
# k -> lose, draw, win
key = {
    'A': ['Z', 'X', 'Y'],
    'B': ['X', 'Y', 'Z'],
    'C': ['Y', 'Z', 'X']
}
points = {'A':1, 'X':1, 'B':2,'Y':2, 'C':3,'Z':3}
outcome = {'X':0,'Y':1,'Z':2}
total = 0
for line in a:
    k1, k2 = line.split()
    chosen = key[k1][outcome[k2]]
    total += points[chosen]
    for i, v in enumerate(key['B']):
        if v == k2:
            total += 3 * i
            break
print(total)
