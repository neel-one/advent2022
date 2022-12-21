import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cmp_to_key
from copy import deepcopy
from typing import Any
from itertools import cycle

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]

@dataclass
class Monkey:
    id: str
    yell: tuple
    expr: Any = None

    def resolved(self):
        return len(self.yell) == 1
    
    def value(self):
        return int(self.yell[0])
    
    def value2(self):
        if self.yell[0].isdigit():
            return NumNode(int(self.yell[0]))
        return VarNode(self.yell[0])

@dataclass
class Expr:
    a: Any = None
    op: Any = None
    b: Any = None

@dataclass
class OpNode:
    op: str

@dataclass
class VarNode:
    value: str

@dataclass
class NumNode:
    value: int

def parse():
    d = {}
    for line in a:
        l = line.split(':')
        m = Monkey(l[0], tuple(l[1].split()))
        d[l[0]] = m
    return d

def solve1(d):
    def rec(id):
        if d[id].resolved():
            return d[id].value()
        a, op, b = d[id].yell
        if op == '+':
            v = rec(a) + rec(b)
        elif op == '-':
            v = rec(a) - rec(b)
        elif op == '*':
            v = rec(a) * rec(b)
        elif op == '/':
            v = rec(a) // rec(b)
        else:
            assert False
        d[id].yell = (v,)
        return d[id].value()
    return rec('root')

def solve2(d):
    def rec(id):
        if d[id].expr is not None:
            return d[id].expr
        if d[id].resolved():
            d[id].expr = d[id].value2()
            return d[id].expr
        a, op, b = d[id].yell
        v = Expr(rec(a),op,rec(b))
        d[id].expr = v
        return v
    return rec('root')

def resolve(expr, try_num = None):
    if try_num is not None and isinstance(expr, VarNode):
        return NumNode(try_num)
    if not isinstance(expr, Expr):
        return expr
    expr.a = resolve(expr.a, try_num)
    expr.b = resolve(expr.b ,try_num)
    if isinstance(expr.a, NumNode) and isinstance(expr.b, NumNode):
        op = expr.op
        if op == '+':
            v = expr.a.value + expr.b.value
        elif op == '-':
            v = expr.a.value - expr.b.value
        elif op == '*':
            v = expr.a.value * expr.b.value
        elif op == '/':
            v = expr.a.value // expr.b.value
        elif op == '=':
            return expr
            v = abs(expr.a.value - expr.b.value) < .00003
        expr = NumNode(v)
        return expr
    return expr

# Notice, We can do this because VarNode only appears once in LHS which guarantees:
# (1) one of values in expr is a NumNode
# (2) we can inverse the operation to move it to RHS
def transform(expr):
    assert isinstance(expr.b, NumNode)
    while not isinstance(expr.a, VarNode):
        a = expr.a.a
        op = expr.a.op
        b = expr.a.b
        assert isinstance(a, NumNode) or isinstance(b, NumNode)
        v, new_a = (a,b) if isinstance(a, NumNode) else (b,a)
        expr.a = new_a
        if op == '+':
            expr.b = Expr(expr.b, '-', v)
        elif op == '-':
            if isinstance(a, NumNode):
                # then we need to multiply LHS by -1
                expr.a = Expr(expr.a, '/', NumNode(-1))
                expr.b = Expr(expr.b, '-', v)
            else:
                expr.b = Expr(expr.b, '+', v)
        elif op == '*':
            expr.b = Expr(expr.b, '/', v)
        elif op == '/':
            expr.b = Expr(expr.b, '*', v)
    return expr

def p(expr):
    if isinstance(expr, NumNode):
        return str(expr.value)
    elif isinstance(expr, VarNode):
        return 'A'
    return f'({p(expr.a)} {expr.op} {p(expr.b)})'

def part1():
    d = parse()
    s =  solve1(d)
    #for v in d:
    #    print(v, d[v].value())
    return s

def f(args):
    i, s = args
    return resolve(deepcopy(s), try_num=i).value

def part2():
    d = parse()
    d['humn'].yell = ('x',)
    y = list(d['root'].yell)
    y[1] = '='
    d['root'].yell = tuple(y)
    s = solve2(d)
    test = deepcopy(s)
    # print(p(resolve(s)))
    s = resolve(s)
    s = transform(s)
    s = resolve(s)
    print(p(s), resolve(test, try_num = s.b.value))


    return s.b.value
    # Multiprocessing is not gonna work hahahaha, nice try tho
    # from multiprocessing import Pool
    # with Pool(16) as p:
    #     l = p.map(f, zip(range(1000000), cycle([s])))
    # return l.index(True)


print(f'Part 1: {part1()}')
print(f'Part 2: {part2()}')

