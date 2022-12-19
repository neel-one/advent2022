import sys

if len(sys.argv) == 1:
    a = [line.strip() for line in open('in').readlines()]
else:
    a = [line.strip() for line in open(__file__.rstrip('.py')).readlines()]
from collections import defaultdict

monkeys = []
i = 0
while i < len(a):
    if 'Monkey' in a[i]:
        m = defaultdict(dict)
        m['start'] = a[i+1].split()[2:]
        for j, v in enumerate(m['start']):
            if ',' in v:
                v = v[:-1]
            m['start'][j] = int(v)
        op = a[i+2].split()[4:]
        if op[0] == '+':
            add = True
        elif op[0] == '*':
            add = False
        if op[1].isdigit():
            if add:
                m['op'] = ('+',int(op[1]))
            else:
                m['op'] = ('*', int(op[1]))
        elif 'old' in op[1]:
            if add:
                m['op'] = ('+',)
            else:
                m['op'] = ('*',)
        m['test'] = int(a[i+3].split()[3])
        m['true'] = int(a[i+4].split()[5])
        m['false'] = int(a[i+5].split()[5])
        m['inspected'] = 0
        i = i + 7
        monkeys.append(m)
    else:
        i += 1

def p():
    for m in monkeys:
        print(m)
        print()

def apply(f, item):
    op = f[0]
    a = item if len(f) == 1 else f[1]
    if op == '+':
        return a + item
    return a * item

div = 1
for m in monkeys:
    div *= m['test']

for r in range(10000):
    for i, m in enumerate(monkeys):
        for item in m['start']:
            level = apply(m['op'], item)
            level = level % div
            if level % m['test'] == 0:
                monkeys[m['true']]['start'].append(level)
            else:
               monkeys[m['false']]['start'].append(level)
            m['inspected'] += 1
        monkeys[i]['start'] = []
    print(f'ROUND {r+1}')

a, b = sorted([m['inspected'] for m in monkeys])[-2:]
print(a*b)
