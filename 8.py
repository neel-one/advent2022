import sys

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]


grid = [];
for line in a:
    grid.append([]);
    for char in line:
        grid[-1].append(int(char))

#print(grid)

sol = 0
highestScenic = 0

for i in range(0, len(grid)):
    for j in range(0, len(grid[i])):
        currentScenic = 1

        a = b = c = d = 0
        for k in range(i + 1, len(grid)):
            a += 1
            if (grid[k][j] >= grid[i][j]):
                foundFlag = False
                break

        for k in range(i - 1, -1, -1):
            b += 1
            if (grid[k][j] >= grid[i][j]):
                foundFlag = False
                break

        for k in range(j + 1, len(grid[i])):
            c += 1
            if (grid[i][k] >= grid[i][j]):
                foundFlag = False
                break

        for k in range(j - 1, -1, -1):
            d += 1
            if (grid[i][k] >= grid[i][j]):
               foundFlag = False
               break
        if a * b * c * d > highestScenic:
            highestScenic = a * b * c *d

print(highestScenic)
