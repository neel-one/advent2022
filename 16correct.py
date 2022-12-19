import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field, replace
from functools import cmp_to_key
from math import prod

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open('16').readlines()]

@dataclass
class Valve:
    name: str
    rate: int
    leads: int

@dataclass
class State:
    pressure: int = 0
    flowing: int = 0
    my_loc: str = 'AA'
    e_loc: str = 'AA'
    open_valves: tuple = tuple()
    steps: tuple = tuple()


def solve(v, limit, elephant = False, prune = 3000):
    def get_start_state():
        s = State()
        for valve in v:
            if v[valve].rate == 0:
                s.open_valves = s.open_valves + (valve,)
                s.steps += (1,)
        return [s]

    def get_next_state(state):
        s = replace(state)
        s.pressure += state.flowing
        return s

    def get_elephant_moves(state, time):
        states = []
        if state.e_loc not in state.open_valves:
            s = replace(state)
            s.flowing += v[state.e_loc].rate
            s.open_valves += (state.e_loc,)
            s.steps += (time+1,)
            states.append(s)
        for neighbor in v[state.e_loc].leads:
            s = replace(state)
            s.e_loc = neighbor
            states.append(s)
        states.append(state)
        return states
    
    # heuristic that uses distance from a node to unopened valves
    def potential(state, time_left, use_e = False):
        q = deque([state.my_loc])
        steps = {v: 0 for v in state.open_valves}
        for i in range(time_left):
            nq = deque()
            while q:
                loc = q.popleft()
                if loc not in state.open_valves:
                    steps[loc] = i
                nq.extend([n for n in v[loc].leads if n not in steps])
            q = nq
        # (time left - steps[node]) * rates
        return sum([(time_left - steps[n])*v[n].rate for n in steps])



    # need some sort of potential function
    #key = lambda s: (s.pressure, s.flowing, len(s.open_valves))
    #key = lambda s: sum([v[valve].rate/steps for valve, steps in zip(s.open_valves, s.steps)])
    most_pressure = 0
    def rec(time, states):
        nonlocal most_pressure
        key = lambda s: (limit-time)*s.flowing + s.pressure + potential(s, limit-time)
        states.sort(key = key, reverse=True)
        if len(states) > prune:
            states = states[:prune]
        
        if time == 8:
            #assert 76 in [s.flowing for s in states]
            pass

        if time == limit:
            for state in states:
                most_pressure = max(most_pressure, state.pressure)
            return 
        new_states = []
        for state in states:
            if state.my_loc not in state.open_valves:
                s = get_next_state(state)
                s.flowing += v[state.my_loc].rate
                s.open_valves += (state.my_loc,)
                s.steps += (time+1,)
                if elephant:
                    new_states.extend(get_elephant_moves(s, time))
                else:
                    new_states.append(s)
            for neighbor in v[state.my_loc].leads:
                s = get_next_state(state)
                s.my_loc = neighbor
                if elephant:
                    new_states.extend(get_elephant_moves(s, time))
                else:
                    new_states.append(s)
            if elephant:
                new_states.extend(
                    get_elephant_moves(get_next_state(state), time))
            else:
                new_states.append(get_next_state(state))
        rec(time+1, new_states)
    rec(0, get_start_state())
    return most_pressure

def parse():
    v = defaultdict(Valve)
    for line in a:
        flow, leads = line.split(';')
        flow = flow.split()
        valve = flow[1]
        rate = int(flow[-1][flow[-1].find('=')+1:])
        leads = leads.split()[4:]
        for i, l in enumerate(leads):
            if l[-1] == ',':
                leads[i] = l[:-1]
        v[valve] = Valve(valve, rate, leads)
    return v

def part1():
    return solve(parse(), limit=30)

def part2():
    return solve(parse(), limit=26, elephant=True, prune=3000)

print(f'Part 1: {part1()}')
print(f'Parts 2: {part2()}')