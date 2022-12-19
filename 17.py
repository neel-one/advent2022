import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cmp_to_key

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]

big = 1000000000000

@dataclass
class Rock:
    data: list

    def __init__(self, *rows):
        self.data = []
        for row in rows:
            self.data.append(list(row))
    
    @property
    def height(self):
        return len(self.data)
    
    @property
    def width(self):
        return len(self.data[0])
    
    def transform(self):
        for row in self.data:
            for i, v in enumerate(row):
                if v == '#':
                    row[i] = '@' 
                elif v == '@':
                    row[i] = '#'
    def serialize(self):
        return ''.join(self.data[0])

@dataclass
class Grid:
    jet_pattern: list
    grid: list = field(default_factory=list)
    highest_rock: int = -1
    it: int = 0
    cache: dict = field(default_factory=dict)
    rock_thrown: int = 0
    skipped: int = 0

    def print(self, prefix=None):
        if prefix is not None:
            print(prefix)
        for row in reversed(self.grid):
            print(f'|{"".join(row)}|')
        print(f'+{"-"*7}+')

    def transform(self, rock, i, j):
        for h, row in enumerate(rock.data):
            for w, data in enumerate(row):
                if self.grid[i+h][j+w] == '@':
                    assert(data == '@')
                    self.grid[i+h][j+w] = '#' 
    
    def fill_rock(self, rock, i, j):
        for h, row in enumerate(rock.data):
            for w, data in enumerate(row):
                self.grid[i+h][j+w] = data
    
    def fall(self, rock, i, j):
        for h, row in enumerate(rock.data):
            for w, data in enumerate(row):
                if self.grid[i+h][j+w] == '@':
                    assert(self.grid[i+h-1][j+w] != '#')
                    self.grid[i+h-1][j+w] = self.grid[i+h][j+w]
                    self.grid[i+h][j+w] = '.'

    def stopped(self, rock, i, j):
        if i == 0:
            return True
        for h, row in enumerate(rock.data):
            for w, data in enumerate(row):
                if data == '@' and self.grid[i+h-1][j+w] == '#':
                    return True
        return False
    
    def apply_jet(self,rock, i, j):
        move = self.jet_pattern[self.it%len(self.jet_pattern)]
        self.it += 1
        if move == '<':
            if j == 0:
                return j
            for h, row in enumerate(rock.data):
                for w, data in enumerate(row):
                    assert(0<=j+w-1<7)
                    if self.grid[i+h][j+w-1] == '#' and self.grid[i+h][j+w] == '@':
                        return j
            for h, row in enumerate(rock.data):
                for w, data in enumerate(row):
                    if self.grid[i+h][j+w] == '@':
                        self.grid[i+h][j+w-1] = self.grid[i+h][j+w]
                        self.grid[i+h][j+w] = '.'
            return j-1
        elif move == '>':
            if j + rock.width >= 7:
                return j
            for h, row in enumerate(rock.data):
                for w in range(len(row)-1,-1,-1):
                    assert(0<=j+w+1<7)
                    if self.grid[i+h][j+w+1] == '#' and self.grid[i+h][j+w] == '@':
                        return j
            for h, row in enumerate(rock.data):
                for w in range(len(row)-1,-1,-1):
                    if self.grid[i+h][j+w] == '@':
                        self.grid[i+h][j+w+1] = self.grid[i+h][j+w]
                        self.grid[i+h][j+w] = '.'
            return j+1 
        else:
            assert(False)

    def add_rock(self, rock: Rock, use_cache = True):
        if not use_cache and (self.rock_thrown-202) % 105 == 0:
            print(self.rock_thrown, self.highest_rock)
        key = None
        check_range = 128
        if use_cache and self.highest_rock >= check_range - 1:
            check = ''
            for i in range(check_range):
                check += ''.join(self.grid[self.highest_rock-i])
            key = (
                check,
                rock.serialize(), 
                self.it%len(self.jet_pattern)
            ) 
            if key in self.cache:
                rock_throw, highest_rock = self.cache[key]
                throw_diff = self.rock_thrown - rock_throw
                height_diff = self.highest_rock - highest_rock + 2
                if height_diff >= check_range:
                    
                    print(f"CACHE HIT at rock {self.rock_thrown} from {self.cache[key]}")
                    # while self.rock_thrown + throw_diff < 2020:
                    #     self.rock_thrown += throw_diff
                    #     #self.highest_rock += height_diff
                    #     self.skipped += height_diff
                    #     print(self.rock_thrown, self.highest_rock + self.skipped)
                    #print(self.rock_thrown, throw_diff)
                    n = (big - self.rock_thrown) // throw_diff
                    if n > 0:
                        self.rock_thrown =  self.rock_thrown + n * throw_diff
                        print(f'N: {n}')
                        self.skipped = n * height_diff
                        self.grid[self.highest_rock] = list(key[0])
        i, j = self.highest_rock + 4, 2
        while len(self.grid) <= i + rock.height - 1:
            self.grid.append(['.' for _ in range(7)])

        self.fill_rock(rock, i, j)
        #self.print()
        
        while True:
            j = self.apply_jet(rock, i, j)

            if self.stopped(rock, i, j):
                #print(f'Stopped on it: {it} with i={i},j={j}')
                self.transform(rock, i, j)
                #self.print()
                break

            # fall 1 unit
            self.fall(rock, i, j)
            i -= 1

            # if self.stopped(rock, i, j):
            #     if i != 0:
            #         j = self.apply_jet(rock, i, j)
            #     #print(f'Stopped on it: {it} with i={i},j={j}')
            #     self.transform(rock, i, j)
            #     #self.print()
            #     break
            
            #self.print()

        #self.highest_rock = max(i + rock.height+1, self.highest_rock)
        for row in range(len(self.grid)-1,-1,-1):
            if '#' in self.grid[row]:
                if key is not None and key not in self.cache:
                    self.cache[key] = (self.rock_thrown, row)
                self.rock_thrown += 1
                self.highest_rock = row
                return

rocks = [
    Rock('####'),
    Rock('.#.','###','.#.'),
    Rock('###','..#','..#'),
    Rock('#','#','#','#'),
    Rock('##','##')
]

jet_pattern = a[0]
def part1():
    grid = Grid(jet_pattern)
    for circuit in range(405):
        for i, rock in enumerate(rocks):
            rock.transform()
            grid.add_rock(rock, False)
            rock.transform()
            if circuit == 4:
                #grid.print('During circuit 4')
                pass
            if circuit * len(rocks) + i+1 >= 2022:
                return grid.highest_rock
        #grid.print(f'After circuit {circuit}')
        print(f'{circuit * len(rocks) + i + 1} rocks have dropped: highest_rock = {grid.highest_rock}')

def part2():
    grid = Grid(jet_pattern)
    while grid.rock_thrown < big:
        for rock in rocks:
            if grid.rock_thrown < big:
                rock.transform()
                grid.add_rock(rock)
                rock.transform()
    return grid.highest_rock + grid.skipped


print(f'Part 1: {part1()+1}')
print(f'Part 2: {part2()+1}')

