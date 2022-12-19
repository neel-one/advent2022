import sys

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]

visited = set()

tails = [(0,0) for _ in range(10)]
for line in a:
    d, v = line.split()
    for _ in range(int(v)):
        hi, hj = tails[0]
        if d == 'R':
            hj += 1
        elif d == 'L':
            hj -= 1
        elif d == 'U':
            hi += 1
        elif d == 'D':
            hi -= 1
        tails[0] = (hi, hj)
        for i in range(1, len(tails)):
            hi, hj = tails[i-1]
            ti, tj = tails[i]
            if ti == hi and abs(hj-tj) >= 2:
                if hj > tj:
                    tj += 1
                else:
                    tj -= 1
            elif tj == hj and abs(hi-ti) >= 2:
                if hi > ti:
                    ti += 1
                else:
                    ti -= 1
            elif tj != hj and ti != hi and (abs(tj-hj) + abs(ti-hi))>=3:
                if hi > ti:
                    ti += 1
                else:
                    ti -= 1
                if hj > tj:
                    tj += 1
                else:
                    tj -= 1
            tails[i] = (ti,tj)
       # print(tails)
        visited.add(tails[-1])
#print(tails)
print(len(visited))

