import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cmp_to_key

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]

@dataclass
class Valve:
    name: str
    rate: int
    leads: list
    visited: set = field(default_factory=set)
    is_open: bool = False

    def can_visit(self, valve, p):
        return (valve,p) not in self.visited

    def add(self, v, p):
        self.visited.add((v,p))

    def remove(self, v, p):
        self.visited.remove((v,p))

def parse():
    d = defaultdict(Valve)
    for line in a:
        flow, leads = line.split(';')
        flow = flow.split()
        valve = flow[1]
        rate = int(flow[-1][flow[-1].find('=')+1:])
        leads = leads.split()[4:]
        for i, l in enumerate(leads):
            if l[-1] == ',':
                leads[i] = l[:-1]
        d[valve] = Valve(valve, rate, leads)
        if rate == 0:
            # a bit hacky but treat 0 rate valves as open
            d[valve].is_open = True
    return d

# at each time step, can either open or go elsewhere
d = parse()
best_so_far = defaultdict(int)
most_pressure = 0
limit = 26
def solve(time, pressure, valve, evalve, flowing, vpath = [], epath = []):
    global d, most_pressure, best_so_far
    left = len([None for v in d.values() if not v.is_open])
    if time == limit:
        #input()
        #print(pressure)
        if pressure >= 2101:
            print(vpath)
            print(epath)
        most_pressure = max(pressure,most_pressure)
        return
    # if limit - time < left//2+1:
    #     #print(time, left//2+1)
    #     return
    # do nothing - probably never worth checking
    #solve(time+1, pressure+flowing, valve, flowing)

    # if pressure+(limit-time)*flowing < most_pressure:
    #     return

    best_so_far[time] = max(best_so_far[time], pressure)
    # heuristic
    if time >= 8 and pressure < .9 * best_so_far[time]:
        return

    # open valve - check if flow > 0
    if not d[valve].is_open and d[valve].rate > 0:
        d[valve].is_open = True
        vpath.append(f'You open valve {valve}')
        #print(f'opening {valve}')
        if not d[evalve].is_open and d[evalve].rate > 0:
            d[evalve].is_open = True
            epath.append(f'E open valve {evalve}')
            solve(time+1, pressure+flowing, valve, evalve, flowing+d[valve].rate+d[evalve].rate)
            d[evalve].is_open = False
            epath.pop()
        
        e_check = False
        for t in d[evalve].leads:
            if d[t].can_visit(evalve, 'e'):
                e_check = True
                d[t].add(evalve, 'e')
                epath.append(f'E moves to {t}')
                solve(time+1,pressure+flowing,valve,t,flowing+d[valve].rate)
                epath.pop()
                d[t].remove(evalve, 'e')
        if not e_check:
            solve(time+1,pressure+flowing,valve,evalve,flowing+d[valve].rate)
        d[valve].is_open = False
        vpath.pop()

    
    # ASSUMPTION to make this code work - always open a valve if you can
    # move to another tunnel - not necessary if all valves are open
    if not all([v.is_open for v in d.values()]):
        v_check = False
        for t in d[valve].leads:
            if d[t].can_visit(valve, 'v'):
                v_check = True
                d[t].add(valve, 'v')
                vpath.append(f'You move to {t}')
                if not d[evalve].is_open and d[evalve].rate > 0:
                    d[evalve].is_open = True
                    epath.append(f'E open valve {evalve}')
                    solve(time+1, pressure+flowing, t,evalve,flowing+d[evalve].rate)
                    epath.pop()
                    d[evalve].is_open = False
                e_check = False
                for s in d[evalve].leads:
                    if d[s].can_visit(evalve, 'e'):
                        e_check = True
                        epath.append(f'E moves to {s}')
                        d[s].add(evalve, 'e')
                        solve(time+1, pressure+flowing, t, s, flowing)
                        epath.pop()
                        d[s].remove(evalve, 'e')
                if not e_check:
                    solve(time+1, pressure+flowing, t, evalve, flowing)
                d[t].remove(valve, 'v')
                vpath.pop()
        if not v_check:
            if not d[evalve].is_open and d[evalve].rate > 0:
                d[evalve].is_open = True
                epath.append(f'E open valve {evalve}')
                solve(time+1, pressure+flowing, valve,evalve,flowing+d[evalve].rate)
                epath.pop()
                d[evalve].is_open = False
            e_check = False
            for s in d[evalve].leads:
                if d[s].can_visit(evalve, 'e'):
                    e_check = True
                    epath.append(f'E moves to {s}')
                    d[s].add(evalve, 'e')
                    solve(time+1, pressure+flowing, valve, s, flowing)
                    epath.pop()
                    d[s].remove(evalve, 'e')
            if not e_check:
                # assert False
                solve(time+1, pressure+flowing, t, evalve, flowing)
    else:
        #print(f'all open: {pressure+(limit-time)*flowing}')
        solve(limit,pressure+(limit-time)*flowing,valve,evalve,flowing)
        #solve(time+1, pressure+flowing, valve, evalve, flowing)

solve(0, 0, 'AA', 'AA',0)
print(most_pressure)



"""
v_options = d[valve].leads +  ['none']
    if not d[valve].is_open:
        v_options = ['open'] + v_options
    
    # ASSUMPTION to make this code work - always open a valve if you can
    # move to another tunnel - not necessary if all valves are open
    if not all([v.is_open for v in d.values()]):
        for v in v_options:
            vopen_flag = False
            vmove_flag = False
            flow = flowing
            vn = v
            if v == 'open' :
                assert not d[valve].is_open
                vopen_flag = True
                d[valve].is_open = True
                vn = valve
                flow += d[valve].rate
            elif v == 'none':
                vn = valve
            else:
                #print(vn, valve)
                if d[vn].can_visit(valve):
                    vmove_flag = True
                    d[vn].add(valve)
                else:
                    continue
            e_options = d[evalve].leads + ['none']
            if not d[evalve].is_open:
                e_options = ['open'] + e_options
            for e in e_options:
                eopen_flag = False
                emove_flag = False
                en = e
                if e == 'open' and not d[evalve].is_open:
                    d[evalve].is_open = True
                    eopen_flag = True
                    en = evalve
                    flow += d[evalve].rate
                elif e == 'none':
                    en = evalve
                else:
                    if d[en].can_visit(evalve):
                        emove_flag = True
                        d[en].add(evalve)
                    else:
                        continue
                solve(time+1, pressure+flowing, vn, en, flow)

                if eopen_flag:
                    d[evalve].is_open = False
                    flow -= d[evalve].rate
                if emove_flag:
                    d[en].remove(evalve)
            
            if vopen_flag:
                d[valve].is_open = False
                flow -= d[valve].rate
            if vmove_flag:
                d[vn].remove(valve)
"""
