import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cmp_to_key

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]

def parse():
    prints = []
    for line in a:
        nums = []
        for word in line.split():
            if word.isdigit():
                nums.append(int(word))
            elif word[:-1].isdigit():
                nums.append(int(word[:-1]))
        assert len(nums) == 7
        prints.append(Blueprint(nums[1], nums[2], (nums[3], nums[4]), (nums[5], nums[6])))
    return prints



@dataclass
class Blueprint:
    ore: int
    clay: int
    obs: tuple
    geode: tuple

    def query(self, x):
        return [self.ore, self.clay, self.obs, self.geode]

    def can_make(self, ore, clay, obs, geo):
        l = []
        if ore >= self.ore:
            l.append(0)
        if ore >= self.clay:
            l.append(1)
        if ore >= self.obs[0] and clay >= self.obs[1]:
            l.append(2)
        if ore >= self.geode[0] and obs >= self.geode[1]:
            l.append(3)
        return l

def solve(blueprint, limit=24, prune = 3000):
    # resource state = (ore, clay, obs, geo)
    # robot state = (ore, clay, obs, geo) robots
    # if we can make all 4 we must, otherwise check different states
    most_geode = 0
    key = lambda s: [-v for pair in zip(tuple(reversed(s[4:])), tuple(reversed(s[:4]))) for v in pair]
    #key = lambda s: [-s[7], -s[3]] #[-v for v in reversed(s[]) ]
    def rec(time, state):
        state.sort(reverse=False, key = lambda s: key(s))
        #state.sort(reverse=True, key = lambda s: tuple(reversed(s[4:])))
        if len(state) > prune:
            state = state[:prune]
            pass
        #print(time, state[:5])
        resources, robots = [s[:4] for s in state], [s[4:] for s in state]
        nonlocal most_geode
        if time == limit:
            for res in resources:
                most_geode = max(most_geode, res[3])
            #print(most_geode)
            return
        new_resources = []
        new_robots = []
        for resource, robot in zip(resources, robots):
            can_make = blueprint.can_make(*resource)
            for c in can_make:
                r = [resource[i] + robot[i] for i in range(4)]
                rob = list(robot)
                rob[c] += 1
                if c == 0:
                    r[0] -= blueprint.ore 
                elif c == 1:
                    r[0] -= blueprint.clay 
                elif c == 2:
                    r[0] -= blueprint.obs[0]
                    r[1] -= blueprint.obs[1]
                elif c == 3:
                    r[0] -= blueprint.geode[0]
                    r[2] -= blueprint.geode[1]
                else:
                    assert False
                # if (2, 9, 0, 0, 1, 3, 0, 0) == resource + robot:
                #     print('here', c)
                #     print(r, rob)
                assert all([x >= 0 for x in r]), r
                new_resources.append(tuple(r))
                new_robots.append(tuple(rob))
            
            # unless we can make all objects, we should try doing nothing
            if len(can_make) < 4:
                r = tuple([resource[i] + robot[i] for i in range(4)])
                new_resources.append(r)
                new_robots.append(robot)
        rec(time+1, [a + b for a,b in zip(new_resources, new_robots)])
    rec(
        0,
        [(0,0,0,0, 1,0,0,0)]
    )
    return most_geode
        
        

def part1():
    prints = parse()
    sol = []
    for _, b in enumerate(prints):
        s = solve(b)
        sol.append(s)
    return sum([(i+1) * sol[i] for i in range(len(prints))]), sol


def part2():
    prints = parse()
    sol = []
    ans = 1
    for i in range(min(3,len(prints))):
        b = prints[i]
        s = solve(b, limit=32, prune=10000)
        sol.append(s)
        ans *= s
    return ans, sol



print(f'Part 1: {part1()}')
#print(f'Part 2: {part2()}')